#!/bin/bash
# Evaluate KITTI results

RESULTS_DIR="$HOME/mobile_robotics_project/results/kitti"
DATASET_DIR="$HOME/mobile_robotics_project/datasets/organized/KITTI"

echo "Evaluating KITTI 08..."

# Fix permissions
sudo chown -R $USER:$USER "$RESULTS_DIR"

# Evaluate with evo
evo_ape kitti \
    "$DATASET_DIR/poses/08.txt" \
    "$RESULTS_DIR/08_keyframes.txt" \
    -va --align --correct_scale \
    --save_results "$RESULTS_DIR/08_ape.zip" 2>/dev/null || \
evo_ape tum \
    <(awk '{print NR*0.1, $4, $8, $12, 0, 0, 0, 1}' "$DATASET_DIR/poses/08.txt") \
    "$RESULTS_DIR/08_keyframes.txt" \
    -va --align --correct_scale

echo ""
echo "Results saved to: $RESULTS_DIR/"
