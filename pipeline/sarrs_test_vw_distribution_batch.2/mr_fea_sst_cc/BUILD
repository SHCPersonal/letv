# Copyright 2014 letv Inc. All Rights Reserved.
# Author: lvjianchun@letv.com

cc_library(
    name = 'abstract_scorer',
    srcs = [
        'abstract_scorer.cc',
        ],
    deps = [
        '//base:base',
        '//recommendation/thrift:recommendation_thrift',
        '//recommendation/thrift:database_thrift',
        '//recommendation/online/engine/base:base',
    ],
)

cc_library(
        name = 'channel_feature_booster',
        srcs = [
                'channel_feature_booster.cc',
               ],
        deps = [
                '//base:base',
                '//recommendation/thrift:recommendation_thrift',
                '//shared/serving/proto:media_doc_info_thrift',
                '//shared/serving/proto:serving_proto',
                '//shared/serving/serving_context:backend_serving_context',
               ],
        link_all_symbols = True,
)

cc_library(
    name = 'freshness_booster',
    srcs = [
        'freshness_booster.cc',
        ],

    deps = [
        ':abstract_scorer',
        '//base:base',
        '//recommendation/thrift:recommendation_thrift',
        '//recommendation/online/engine/base:result_info_helper',
        '//shared/serving/proto:media_doc_info_thrift',
        '//shared/serving/proto:serving_proto',
        '//shared/serving/serving_context:backend_serving_context',
        '//util/polyline:polyline',
    ],
    link_all_symbols=True,
)

cc_library(
    name = 'hot_word_booster',
    srcs = [
        'hot_word_booster.cc',
        ],

    deps = [
        ':abstract_scorer',
        '//base:base',
        '//recommendation/thrift:recommendation_thrift',
        '//recommendation/online/engine/base:result_info_helper',
        '//shared/serving/proto:media_doc_info_thrift',
        '//shared/serving/proto:serving_proto',
        '//shared/serving/serving_context:backend_serving_context',
    ],
    link_all_symbols=True,
)

cc_library(
    name = 'static_attribute_booster',
    srcs = [
        'static_attribute_booster.cc',
        ],

    deps = [
        ':abstract_scorer',
        '//base:base',
        '//recommendation/thrift:recommendation_thrift',
        '//recommendation/online/engine/base:result_info_helper',
        '//shared/serving/proto:media_doc_info_thrift',
        '//shared/serving/proto:serving_proto',
        '//shared/serving/serving_context:backend_serving_context',
        '//util/polyline:polyline',
    ],
    link_all_symbols=True
)

cc_library(
    name = 'anti_vulgarity_booster',
    srcs = [
        'anti_vulgarity_booster.cc',
        ],

    deps = [
        ':abstract_scorer',
        '//base:base',
        '//recommendation/thrift:recommendation_thrift',
        '//shared/serving/proto:serving_proto',
        '//shared/serving/serving_context:backend_serving_context',
        '//util/polyline:polyline',
    ],
    link_all_symbols=True,
)

cc_library(
    name = 'source_booster',
    srcs = [
        'source_booster.cc',
        ],

    deps = [
        ':abstract_scorer',
        '//base:base',
        '//recommendation/thrift:recommendation_thrift',
        '//shared/serving/proto:serving_proto',
        '//shared/serving/serving_context:backend_serving_context',
    ],
    link_all_symbols=True,
)

cc_library(
    name = 'feature_booster',
    srcs = [
        'feature_booster.cc',
        ],

    deps = [
        ':abstract_scorer',
        '//base:base',
        '//recommendation/thrift:recommendation_thrift',
        '//shared/serving/proto:serving_proto',
        '//shared/serving/serving_context:backend_serving_context',
    ],
    link_all_symbols=True,
)

cc_library(
    name = 'exposure_and_not_watch_booster',
    srcs = [
        'exposure_and_not_watch_booster.cc',
        ],

    deps = [
        ':abstract_scorer',
        '//base:base',
        '//recommendation/thrift:recommendation_thrift',
        '//shared/serving/proto:serving_proto',
        '//shared/serving/serving_context:backend_serving_context',
    ],
    link_all_symbols=True,
)

cc_library(
    name = 'user_collection_booster',
    srcs = [
        'user_collection_booster.cc',
        ],

    deps = [
        ':abstract_scorer',
        '//base:base',
        '//recommendation/thrift:recommendation_thrift',
        '//shared/serving/proto:serving_proto',
        '//shared/serving/serving_context:backend_serving_context',
    ],
    link_all_symbols=True,
)

cc_library(
    name = 'scorer',
    srcs = [
        'default_scorer.cc',
        'default_scorer_creator.cc',
        'vec_scorer.cc',
        'vec_scorer_creator.cc',
        'personal_profile_scorer.cc',
        'personal_profile_scorer_creator.cc',
        'feature_aggregation_scorer.cc',
        'feature_aggregation_scorer_creator.cc',
		'Personalized_ctr_predict_scorer.cc',
		'Personalized_ctr_predict_scorer_creator.cc',
		'Personalized_ctr_predict_feature_builder.cc'
    ],

    deps = [
        ':channel_feature_booster',
        ':abstract_scorer',
        ':freshness_booster',
        ':static_attribute_booster',
        ':anti_vulgarity_booster',
        ':source_booster',
        ':feature_booster',
        ':hot_word_booster',
        ':exposure_and_not_watch_booster',
        ':user_collection_booster',
        '//base:base',
        '//recommendation/online/engine/common:user_profile_util',
        '//recommendation/online/engine/common:feature_selector',
        '//recommendation/online/database_proxy:sst_file_loader',
        '//recommendation/online/engine/base:feature_help',
        '//recommendation/thrift:recommendation_thrift',
        '//recommendation/thrift:database_thrift',
        '//shared/serving/proto:media_doc_info_thrift',
        '//shared/serving/proto:serving_proto',
        '//shared/serving/proto:user_profile_thrift',
        '//shared/serving/serving_context:request_user_profile',
        '//shared/serving/serving_context:serving_feature',
    ],
    link_all_symbols=True
)
cc_library(
   name = 'feature_build_lib',
   srcs = [
        'Personalized_ctr_predict_feature_builder.cc',
   ],
   deps = [
        '//base:base',
   ],
   link_all_symbols=True
)
swig_library(
		name = 'feature_build',
		srcs = [
				'feature_build.i'
		],
		deps = [
				':feature_build_lib'
		],
		
)
