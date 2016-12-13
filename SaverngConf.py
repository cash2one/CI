#tera schemas per linkbase tables
DLB_LINKBASE_SCHEMA="""<rawkey=binary,splitsize=4096,wal=on> {
      lg0 <storage=flash,blocksize=32,sst_size=8,use_memtable_on_leveldb=true,memtable_ldb_write_buffer_size=1000,memtable_ldb_block_size=4> {
          RAW <maxversions=1,minversions=1,ttl=0,type=bytes>
      }
  }"""
L2LINKBASE_SCHEMA="""<rawkey=binary, splitsize=512, mergesize=0> {
    lg0 <storage=flash,compress=snappy,blocksize=32,use_memtable_on_leveldb=true,memtable_ldb_write_buffer_size=1,memtable_ldb_block_size=4> {
        RAW <maxversions=1,minversions=1,ttl=0>
    }
}"""

BOGUS_RESET_SCHEMA="""<rawkey=binary,splitsize=100,mergesize=0> {
      lg0 <storage=flash,blocksize=4,sst_size=8,use_memtable_on_leveldb=true,memtable_ldb_write_buffer_size=1000,memtable_ldb_block_size=4> {
          cf <maxversions=1,minversions=1,ttl=0,type=bytes>
      }
  }"""
PROC_SCHEMA="""<rawkey=binary,splitsize=100,mergesize=0> {
      lg0 <storage=flash,blocksize=4,sst_size=8,use_memtable_on_leveldb=true,memtable_ldb_write_buffer_size=1000,memtable_ldb_block_size=4> {
          cf <maxversions=1,minversions=1,ttl=0,type=bytes>
      }
  }"""

DICT_META_SCHEMA="""<rawkey=binary, splitsize=100, mergesize=0> {
    lg0 <storage=flash,compress=snappy,blocksize=4,use_memtable_on_leveldb=true> {
        cf <maxversions=1,minversions=1,ttl=0>
    }
}"""

DOMAIN_STAT_SCHEMA="""<rawkey=binary,splitsize=240,mergesize=0,wal=on> {
      lg0 <storage=flash,blocksize=32,sst_size=8,use_memtable_on_leveldb=true,memtable_ldb_write_buffer_size=100,memtable_ldb_block_size=4> {
          cf<maxversions=1,minversions=1,ttl=0,type=bytes>
      }
  }
"""

DOMAIN_LIMIT_SCHEMA="""<rawkey=binary,splitsize=240,mergesize=0,wal=on> {
      lg0 <storage=flash,blocksize=32,sst_size=8,use_memtable_on_leveldb=true,memtable_ldb_write_buffer_size=100,memtable_ldb_block_size=4> {
          cf<maxversions=1,minversions=1,ttl=0,type=bytes>
      }
  }"""

SITE_STAT_SCHEMA="""<rawkey=binary,splitsize=240,mergesize=0,wal=on> {
      lg0 <storage=flash,blocksize=32,sst_size=8,use_memtable_on_leveldb=true,memtable_ldb_write_buffer_size=100,memtable_ldb_block_size=4> {
          cf<maxversions=1,minversions=1,ttl=0,type=bytes>
      }
    }"""
SITE_LIMIT_SCHEMA="""<rawkey=binary,splitsize=240,mergesize=0,wal=on> {
      lg0 <storage=flash,blocksize=32,sst_size=8,use_memtable_on_leveldb=true,memtable_ldb_write_buffer_size=100,memtable_ldb_block_size=4> {
          cf<maxversions=1,minversions=1,ttl=0,type=bytes>
      }
  }"""

TEXT_DICT_SCHEMA="""<rawkey=binary,splitsize=240,mergesize=0,wal=on> {
      lg0 <storage=flash,blocksize=32,sst_size=8,use_memtable_on_leveldb=true,memtable_ldb_write_buffer_size=100,memtable_ldb_block_size=4> {
          cf<maxversions=1,minversions=1,ttl=0,type=bytes>
      }
  }"""

DICT_META_BOUNDARY = 'saverng_boundary_dict'

SAVERNG_ZK_ADDR_LIST = 'nmg01-ps-ps-hunbu1wm2284.nmg01.baidu.com:18682'

FIELDS = 'all'
BEGIN_URL='!.!'
END_URL='~.~'

LB_FIELD_NAMES = ['m_url', 'm_etag', 'm_url_sign1', 'm_url_sign2', 'm_site_sign1', 'm_site_sign2', 'm_domain_sign1', 'm_domain_sign2', 'm_ip', 'm_in_date', 'm_last_mod_time', 'page_len', 'crawl', 'last_mod', 'publish_time', 'history', 'history.not_use', 'history.ok', 'history.mod', 'history.notmod', 'history.fail_1', 'history.fail_lastack', 'history.fail_3', 'history.fail_2', 'history.fail_4', 'history.delete', 'rank_in', 'isselect', 'sel_time', 'forceCHK', 'urlnew', 'failno', 'pt0_num', 'pt0_clear', 'hub_depth', 'not_mod', 'code_type', 'pre_del', 'link_depth', 'out_link', 'http11', 'chn_depth', 'url_level', 'dir_depth', 'page_type', 'page_type_offline', 'rank_out', 'url_type', 'age_added', 'forceGET', 'lsen_check', 'preurl_type', 'link_depth_true', 'anchor_type', 'preurl_depth', 'del_reason', 'weight', 'no_limit', 'pv_num', 'limited', 'bypassno', 'online', 'extern_link', 'inner_link', 'pre_pagesign', 'm_preurl', 'm_anchor', 'ptnumber', 'pattern_abs_get', 'pattern_abs_chk', 'pattern_rel_get', 'pattern_rel_chk', 'follow_spec', 'csen_check', 'density_daily', 'density_sum', 'expect_inc', 'expire_idx', 'premerge_flag', 'mod_hist', 'del_flag', 'is_replace', 'discard_flag', 'click', 'sobar', 'chk_all_new', 'chk_all_res', 'chk_self_new', 'chk_self_res', 'pattern_abs_get_offline', 'pattern_abs_chk_offline', 'pattern_rel_get_offline', 'pattern_rel_chk_offline', 'last_follow_all_days', 'last_follow_site_days', 'last_follow_domain_days', 'last_fail_begin_days', 'linkuniq_version', 'preurl_relation_type', 'is_need_mask', 'simhash', 'authority', 'real_typenum', 'index_rank', 'update_rank', 'pagerank', 'tmp_not_fail_lastack', 'tmp_set_pattern', 'crawlhist0', 'crawlhist1', 'crawlhist2', 'crawlhist3', 'crawlhist4', 'crawlhist5', 'crawlhist6', 'crawlhist7', 'pr_insite', 'pr_time', 'page_crawl_time', 'link_src', 'link_src_level', 'crawltype', 'crawlconf', 'pattern_sign', 'bogus_hist', 'CentralLen', 'preurl_value', 'link_src_type', 'fresh_value', 'StructSign', 'ContentLength', 'TitleLength', 'PageLength', 'SexFactor', 'Politicalfactor', 'Wise', 'cont_chk_bad_gain_problem', 'cont_chk_change_gain_problem', 'cont_chk_good_gain_problem', 'cont_chk_mine_gain_problem', 'PageNum', 'BBSReply', 'IsFirstPage', 'm_preurl_value_info', 'mdoc_type', 'layer', 'tm_sign', 'long_sign', 'show_num', 'chk_diff', 'select_level', 'select_weight', 'strategy_map', 'sample_map', 'preurl_langtype', 'lang_type', 'protocol', 'wap_dup', 'wap_dup_offline', 'zombie_set', 'zombie_his', 'zombie_trans', 'robots_info', 'redir_type', 'expect_to_url_md5', 'old_to_url_md5', 'wise_weight', 'user_data_src0', 'user_data_src1', 'user_data_src2', 'user_data_src3', 'avg_query_pos', 'query_freq_sum', 'avg_user_focus_time', 'url_anchor_match', 'crossindex_value', 'store_level', 'network_ctrl', 'abnormal_time', 'abnormal_count', 'abnormal', 'patch_type', 'expr', 'exurl','image_type', 'cache_dest', 'share_pageview_num', 'ml_is_dead_lable', 'ml_is_deadlink_protocol', 'ml_is_deadlink_content', 'ml_is_deadlink_redir', 'ml_is_over_flow_label', 'ml_longterm_garbage_num', 'ml_indexfeature', 'ml_is_weight10_label', 'ml_is_rubbish', 'ml_err_type', 'ml_length_key_value', 'ml_total_key_value', 'ml_pr_timenum_grow', 'ml_pr_downloadlink_num', 'ml_pr_videonum', 'ml_is_turn_page', 'ml_central_len', 'ml_tide_score', 'ml_taoke_score', 'ml_resvalidity_score', 'ml_qa_level', 'ml_is_park', 'ml_pv_score', 'ml_pv_rank', 'ml_rbm_label', 'ml_rbm_predict_prob', 'ml_rbm_invlink', 'ml_rbm_feature', 'ml_diff_len_xpath', 'ml_dedup_xpath_num', 'ml_anc_len', 'ml_txt_len', 'ml_anx_sum', 'ml_txt_sum', 'ml_dedup_type', 'ml_max_tag_len', 'ml_anc_url_lcs_ratio', 'ml_ptdef_number', 'ml_userdata_freq_q_sobar', 'ml_userdata_freq_q_browser', 'ml_userdata_freq_q_share_pv', 'ml_userdata_freq_q_statistics', 'ml_userdata_freq_q_competition', 'ml_userdata_freq_q_refer_competition', 'ml_userdata_freq_q_sum', 'ml_aver_query_pos', 'ml_query_freq_sum', 'ml_aver_userfocus_t', 'ml_q_u_hot_value', 'ml_q_u_rare_value', 'ml_pt_avg_q_u_hot_val', 'ml_pt_avg_q_u_rare_val', 'ml_spam_num', 'ml_show_time', 'ml_click_time', 'sitemap_priority', 'qu_rare', 'qu_freq', 'entity_type', 'entity_priority','aladdin_priority', 'ml_urllen_path_split', 'ml_urllencot_path_split_site', 'ml_urllencot_path_split_pt', 'cache_dest_modify','force_crawl_priority', 'pr_insite_offline', 'sitemap_lastmodtime', 'sitemap_changefreq', 'sitemap_sign', 'sitemap_schemaid', 'statpt_sign', 'pdtest_sign', 'eftest_sign', 'userdata_level', 'userdata_src', 'weight_re_calc', 'click_num','exprotocol','image_weight','cache_id', "daily_spectrum", "next_select_time", "exdata_first_src", "exdata_cur_src", "exdata_src", "exdata_freq", "exdata_stay_time", "exdata_freq_q_sobar", "exdata_freq_q_browser", "exdata_freq_q_share_pv", "exdata_freq_q_statistics", "exdata_freq_q_competition", "first_get_ok_time", "link_weight", "failno_v2", "old_density_daily", "first_found_time", "first_push_time", "first_spider_found_time", "pageclassify", "uncrawl_url_wise_predict", "m_hubpreurl", "first_crawl_succ_time", "redir_url", "delete_time","sf_render_type","last_merge_time","title"]
NO_NEED_FIELD = []
