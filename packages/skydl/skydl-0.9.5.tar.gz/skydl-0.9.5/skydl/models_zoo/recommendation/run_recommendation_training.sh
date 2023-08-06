#!/bin/bash
echo start `date`
export PATH=/usr/local/cuda/bin:/home/user/anaconda3/bin:$PATH;LD_LIBRARY_PATH=/usr/local/cuda/lib64:/usr/local/cuda/lib
# exec python script
python /home/user/ai_trained_models/recommend_ranking/wide_and_deep_tf_keras_modelv2.py >> ~/ai_training_logs/wide_and_deep_recommendation.log 2>&1 \
echo starting training ok!