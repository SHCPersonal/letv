%module feature_build
%include "std_string.i"
%include "std_vector.i"
%include "std_map.i"
%include "std_pair.i"
%{
#define SWIG_FILE_WITH_INIT
#include "recommendation/online/engine/scorer/Personalized_ctr_predict_feature_builder.h"
%}



namespace std {
    %template(RawFeatureData) map<string, string>;
    %template(TmpData) vector<string>;
};

%include "recommendation/online/engine/scorer/Personalized_ctr_predict_feature_builder.h"
