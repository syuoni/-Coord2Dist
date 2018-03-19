# -*- coding: utf-8 -*-
import numpy as np
from scipy import stats

def calc_lda_theta(lda_md, corpus):
    '''calc matrix theta, with shape of (n_doc, n_topic)
    probability of each topic appearing in each document
    lda_md do not keep information of training corpus, so we need to do inference 
    for training corpus again. 
    '''
    gamma, _ = lda_md.inference(corpus, collect_sstats=False)    
    theta = gamma / np.sum(gamma, axis=1, keepdims=True)
    return theta

def calc_lda_phi(lda_md):
    '''calc matrix phi, with shape of (n_topic, n_volcabulary)
    probability of each word appearing in each topic
    lda.state only keeps information of eta-vector and sstats-matrix
    lda.state.lambda = lda.state.eta + lda.state.sstats
    '''
    lda_lambda = lda_md.state.get_lambda()
    phi = lda_lambda / np.sum(lda_lambda, axis=1, keepdims=True)
    return phi

def calc_lda_log2_perplexity(lda, corpus):
    '''per-word perplexity
    conditional on theta and phi
    note: lda.log_perplexity is a bound of perplexity, not perplexity itself
    ref: 
        http://blog.csdn.net/pirage/article/details/9368535
        https://en.wikipedia.org/wiki/Perplexity
    '''
    theta = calc_lda_theta(lda, corpus)
    phi = calc_lda_phi(lda)
    
    # log of probability of each word appearing in each document, (n_doc, n_volcabulary)
    log2_prob_word_in_doc = np.log2(theta.dot(phi))
    
    # per-word probability
    log2_pw_prob_seq = []
    for doc_id, doc in enumerate(corpus):
        sent_length = np.sum([n_w for w_id, n_w in doc])
        sent_log2_prob = np.sum([log2_prob_word_in_doc[doc_id, w_id] * n_w for w_id, n_w in doc])
        
        log2_pw_prob_seq.append(sent_log2_prob / sent_length)
    return -np.mean(log2_pw_prob_seq)

def calc_lda_log_likelihood(lda, corpus):
    '''full corpus likelihood
    conditional on theta and phi
    '''
    theta = calc_lda_theta(lda, corpus)
    phi = calc_lda_phi(lda)
    
    # log of probability of each word appearing in each document, (n_doc, n_volcabulary)
    log_prob_word_in_doc = np.log(theta.dot(phi))
    
    log_prob_sum = 0.
    for doc_id, doc in enumerate(corpus):
        log_prob_sum += np.sum([log_prob_word_in_doc[doc_id, w_id] * n_w for w_id, n_w in doc])
    return log_prob_sum

# TODO: ??
def calc_lda_posterior_prob(lda, corpus):
    '''posterior probability is just the likelihood which is conditional on topic 
    number (or alpha and beta), rather than theta and phi.
    ref:
        Griffiths T L, Steyvers M. Finding scientific topics[J]. Proceedings of the National academy of Sciences, 2004, 101(suppl 1): 5228-5235.
    '''
    theta = calc_lda_theta(lda, corpus)
    phi = calc_lda_phi(lda)
    
    # shape = (n_doc, n_volcabulary)
#    log_theta_phi = np.log(theta.dot(phi))
    
    # add prior probability
    log_phi_prior = np.array([stats.dirichlet.logpdf(phi_k, lda.eta) for phi_k in phi])
    log_theta_prior = np.array([stats.dirichlet.logpdf(theta_m, lda.alpha) for theta_m in theta])
    #??    
    return np.sum(log_phi_prior) + np.sum(log_theta_prior) + calc_lda_log_likelihood(lda, corpus)
    
def calc_avg_cosine(lda):
    '''ref: 曹娟, 张勇东, 李锦涛, 等. 一种基于密度的自适应最优化 LDA 模型选择方法[J]. 计算机学报, 2008, 31(10).
    '''
    phi = calc_lda_phi(lda)
    n_topic = phi.shape[0]
    # inner product, shape of (n_topic, n_topic)
    inner_prod = phi.dot(phi.T)
    
    mod = np.sum(phi**2, axis=1) ** 0.5
    cosine = inner_prod / (mod * mod[:, None])
    avg_cosine = (np.sum(cosine)-n_topic) / (n_topic * (n_topic-1))
    return avg_cosine