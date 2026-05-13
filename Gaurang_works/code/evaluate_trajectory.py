#!/usr/bin/env python3
"""Simple trajectory evaluation - no evo dependency"""
import numpy as np
import sys
import os

def load_tum_trajectory(filename):
    """Load TUM format trajectory"""
    data = np.loadtxt(filename)
    timestamps = data[:, 0]
    positions = data[:, 1:4]
    quaternions = data[:, 4:8]
    return timestamps, positions, quaternions

def compute_ate(gt_pos, est_pos):
    """Compute Absolute Trajectory Error"""
    # Simple alignment by centering
    est_centered = est_pos - est_pos[0]
    gt_centered = gt_pos - gt_pos[0]
    
    # Compute errors
    errors = np.linalg.norm(gt_centered - est_centered, axis=1)
    
    rmse = np.sqrt(np.mean(errors**2))
    mean_error = np.mean(errors)
    median_error = np.median(errors)
    max_error = np.max(errors)
    min_error = np.min(errors)
    std_error = np.std(errors)
    
    return {
        'rmse': rmse,
        'mean': mean_error,
        'median': median_error,
        'max': max_error,
        'min': min_error,
        'std': std_error,
        'errors': errors
    }

def plot_trajectories(gt_pos, est_pos, output_file='trajectory.pdf'):
    """Plot 2D trajectories"""
    try:
        import matplotlib
        matplotlib.use('Agg')  # Use non-interactive backend
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(10, 8))
        
        plt.plot(gt_pos[:, 0], gt_pos[:, 1], 'k-', linewidth=2, label='Ground Truth')
        plt.plot(est_pos[:, 0], est_pos[:, 1], 'r--', linewidth=1.5, label='Estimated')
        
        # Mark start and end
        plt.plot(gt_pos[0, 0], gt_pos[0, 1], 'go', markersize=10, label='Start')
        plt.plot(gt_pos[-1, 0], gt_pos[-1, 1], 'ro', markersize=10, label='End')
        
        plt.xlabel('X (m)', fontsize=14)
        plt.ylabel('Y (m)', fontsize=14)
        plt.title('Trajectory Comparison', fontsize=16)
        plt.legend(fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.axis('equal')
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Plot saved to: {output_file}")
        return True
    except Exception as e:
        print(f"⚠ Plotting failed: {e}")
        print("  (Metrics are still computed correctly)")
        return False

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 evaluate_trajectory.py <groundtruth.txt> <estimated.txt>")
        sys.exit(1)
    
    gt_file = sys.argv[1]
    est_file = sys.argv[2]
    
    # Check files exist
    if not os.path.exists(gt_file):
        print(f"Error: {gt_file} not found")
        sys.exit(1)
    if not os.path.exists(est_file):
        print(f"Error: {est_file} not found")
        sys.exit(1)
    
    # Load trajectories
    print("Loading trajectories...")
    gt_time, gt_pos, gt_quat = load_tum_trajectory(gt_file)
    est_time, est_pos, est_quat = load_tum_trajectory(est_file)
    
    print(f"  Ground truth: {len(gt_pos)} poses, {np.linalg.norm(gt_pos[-1] - gt_pos[0]):.3f}m path length")
    print(f"  Estimated:    {len(est_pos)} poses, {np.linalg.norm(est_pos[-1] - est_pos[0]):.3f}m path length")
    
    # Compute metrics
    print("\nComputing metrics...")
    results = compute_ate(gt_pos, est_pos)
    
    # Display results
    print("\n" + "="*60)
    print(" ABSOLUTE TRAJECTORY ERROR (ATE)")
    print("="*60)
    print(f"  RMSE:    {results['rmse']:.6f} m")
    print(f"  Mean:    {results['mean']:.6f} m")
    print(f"  Median:  {results['median']:.6f} m")
    print(f"  Std Dev: {results['std']:.6f} m")
    print(f"  Min:     {results['min']:.6f} m")
    print(f"  Max:     {results['max']:.6f} m")
    print("="*60)
    
    # Save results to file
    with open('ate_results.txt', 'w') as f:
        f.write("Absolute Trajectory Error (ATE)\n")
        f.write("="*60 + "\n")
        f.write(f"RMSE:    {results['rmse']:.6f} m\n")
        f.write(f"Mean:    {results['mean']:.6f} m\n")
        f.write(f"Median:  {results['median']:.6f} m\n")
        f.write(f"Std Dev: {results['std']:.6f} m\n")
        f.write(f"Min:     {results['min']:.6f} m\n")
        f.write(f"Max:     {results['max']:.6f} m\n")
    print("\n✓ Results saved to: ate_results.txt")
    
    # Plot
    print("\nGenerating plot...")
    plot_trajectories(gt_pos, est_pos)
    
    print("\n✓ Done!")

if __name__ == '__main__':
    main()
