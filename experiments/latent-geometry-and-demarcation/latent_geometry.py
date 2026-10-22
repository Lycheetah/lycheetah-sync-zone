#!/usr/bin/env python3
"""
Latent Geometry & Hyperspherical Trajectory Analyzer
Node 07: AURA-PHENOMENOLOGIST · Lycheetah Sync Zone
Human Architect & Teleological Sovereign: Mackenzie Conor James Clark (Mac)

Empirical verification of:
1. Concentration of measure on hyperspherical shell S^{D-1}(sqrt(D))
2. Asymptotic pairwise cosine orthogonality: cos(theta) ~ N(0, 1/D)
3. Geodesic slerp vs. Euclidean lerp dimensional collapse
4. Isometric Riemannian Brownian motion on S^{D-1} via the Exponential Map
5. Activation distributions, temperature entropy scaling, and score flow relaxation
"""

import math
from typing import Dict, List, Optional, Tuple, Union
import numpy as np
from scipy import stats


class HypersphericalLatentSpace:
    """
    Mathematical engine analyzing high-dimensional Gaussian prior geometries,
    hyperspherical concentration of measure, and geodesic walks.
    """

    def __init__(self, seed: Optional[int] = 42):
        self.rng = np.random.default_rng(seed)

    def sample_gaussian(self, n_samples: int, dim: int) -> np.ndarray:
        """Samples n points from isotropic standard normal N(0, I_dim)."""
        return self.rng.standard_normal((n_samples, dim))

    def compute_radial_statistics(self, n_samples: int, dim: int) -> Dict[str, float]:
        """
        Computes empirical radial statistics of standard Gaussian samples in R^dim
        and compares with theoretical Chi-distribution properties.
        """
        samples = self.sample_gaussian(n_samples, dim)
        radii = np.linalg.norm(samples, axis=1)

        emp_mean = float(np.mean(radii))
        emp_var = float(np.var(radii, ddof=1))
        emp_std = float(np.std(radii, ddof=1))

        # Analytical expectation for Chi(dim): sqrt(2) * Gamma((dim+1)/2) / Gamma(dim/2)
        # Using 2nd order Taylor approximation: sqrt(dim) * (1 - 1/(4*dim) + O(dim^-2))
        theo_mean_approx = math.sqrt(dim) * (1.0 - 1.0 / (4.0 * dim))
        theo_var_approx = 0.5  # Asymptotically independent of dim!
        theo_rel_thickness = (math.sqrt(theo_var_approx) / math.sqrt(dim))

        emp_rel_thickness = emp_std / emp_mean

        return {
            "dim": dim,
            "n_samples": n_samples,
            "empirical_mean_radius": emp_mean,
            "theoretical_mean_radius": theo_mean_approx,
            "mean_radius_error": abs(emp_mean - theo_mean_approx),
            "empirical_radius_variance": emp_var,
            "theoretical_radius_variance": theo_var_approx,
            "variance_error": abs(emp_var - theo_var_approx),
            "empirical_relative_thickness": emp_rel_thickness,
            "theoretical_relative_thickness": theo_rel_thickness,
        }

    def compute_pairwise_cosine_geometry(self, n_samples: int, dim: int) -> Dict[str, float]:
        """
        Computes pairwise cosine similarities between independent Gaussian vectors
        and tests against asymptotic distribution N(0, 1/dim).
        """
        samples = self.sample_gaussian(n_samples, dim)
        norms = np.linalg.norm(samples, axis=1, keepdims=True)
        unit_vecs = samples / np.maximum(norms, 1e-12)

        # Compute upper triangular pairwise cosine similarities
        dot_matrix = unit_vecs @ unit_vecs.T
        triu_indices = np.triu_indices(n_samples, k=1)
        cosines = dot_matrix[triu_indices]

        emp_mean = float(np.mean(cosines))
        emp_var = float(np.var(cosines, ddof=1))
        theo_var = 1.0 / float(dim)

        # Kolmogorov-Smirnov test against normal N(0, 1/dim)
        ks_stat, p_val = stats.kstest(cosines, "norm", args=(0.0, math.sqrt(theo_var)))

        # Lévy's Concentration bound: fraction of pairs within 3 / sqrt(dim)
        three_sigma = 3.0 / math.sqrt(dim)
        fraction_within_3sigma = float(np.mean(np.abs(cosines) <= three_sigma))

        return {
            "dim": dim,
            "n_pairs": len(cosines),
            "empirical_mean_cosine": emp_mean,
            "empirical_var_cosine": emp_var,
            "theoretical_var_cosine": theo_var,
            "variance_ratio": emp_var / theo_var,
            "ks_statistic": float(ks_stat),
            "ks_p_value": float(p_val),
            "three_sigma_bound": three_sigma,
            "fraction_within_3sigma": fraction_within_3sigma,
        }

    @staticmethod
    def lerp(z0: np.ndarray, z1: np.ndarray, t: Union[float, np.ndarray]) -> np.ndarray:
        """Euclidean linear interpolation: (1-t) * z0 + t * z1."""
        if isinstance(t, np.ndarray):
            t = t[:, np.newaxis]
        return (1.0 - t) * z0 + t * z1

    @staticmethod
    def slerp(z0: np.ndarray, z1: np.ndarray, t: Union[float, np.ndarray]) -> np.ndarray:
        """
        Spherical linear interpolation along the great circle arc on S^{D-1}.
        Preserves radius exactly: ||slerp(z0, z1, t)|| == ||z0|| (for ||z0|| == ||z1||).
        """
        norm0 = np.linalg.norm(z0)
        norm1 = np.linalg.norm(z1)
        r = norm0

        u0 = z0 / max(norm0, 1e-12)
        u1 = z1 / max(norm1, 1e-12)

        dot = float(np.clip(np.dot(u0, u1), -1.0, 1.0))
        theta = math.acos(dot)

        if abs(theta) < 1e-7:
            # Collinear or identical vectors
            return np.tile(z0, (len(t), 1)) if isinstance(t, np.ndarray) else z0.copy()

        sin_theta = math.sin(theta)

        if isinstance(t, (int, float)):
            w0 = math.sin((1.0 - t) * theta) / sin_theta
            w1 = math.sin(t * theta) / sin_theta
            return w0 * z0 + w1 * (z1 * (r / max(norm1, 1e-12)))

        t_arr = np.asarray(t, dtype=float)[:, np.newaxis]
        w0 = np.sin((1.0 - t_arr) * theta) / sin_theta
        w1 = np.sin(t_arr * theta) / sin_theta
        res = w0 * z0 + w1 * (z1 * (r / max(norm1, 1e-12)))
        return res

    def compare_lerp_vs_slerp(
        self, dim: int, n_steps: int = 101
    ) -> Dict[str, Union[float, np.ndarray]]:
        """
        Compares Euclidean lerp vs Geodesic slerp between two sampled latent vectors
        and proves the midpoint dimensional collapse.
        """
        samples = self.sample_gaussian(2, dim)
        # Project exactly onto theoretical shell radius R = sqrt(dim)
        r = math.sqrt(dim)
        z0 = samples[0] / np.linalg.norm(samples[0]) * r
        z1 = samples[1] / np.linalg.norm(samples[1]) * r

        t_values = np.linspace(0.0, 1.0, n_steps)
        lerp_path = self.lerp(z0, z1, t_values)
        slerp_path = self.slerp(z0, z1, t_values)

        lerp_norms = np.linalg.norm(lerp_path, axis=1)
        slerp_norms = np.linalg.norm(slerp_path, axis=1)

        mid_idx = n_steps // 2
        mid_lerp_norm = float(lerp_norms[mid_idx])
        mid_slerp_norm = float(slerp_norms[mid_idx])

        # Theoretical prediction for nearly orthogonal endpoints:
        # ||z_lerp(0.5)|| = r / sqrt(2) approx 0.7071 * r
        dot = float(np.dot(z0, z1) / (r * r))
        theo_mid_norm = r * math.sqrt(0.5 * (1.0 + dot))

        # Deviation in units of standard deviation sigma_R = 1 / sqrt(2)
        sigma_r = 1.0 / math.sqrt(2.0)
        collapse_in_sigmas = (r - mid_lerp_norm) / sigma_r

        slerp_norm_max_err = float(np.max(np.abs(slerp_norms - r)))

        return {
            "dim": dim,
            "shell_radius": r,
            "midpoint_lerp_norm": mid_lerp_norm,
            "theoretical_midpoint_lerp_norm": theo_mid_norm,
            "midpoint_lerp_ratio": mid_lerp_norm / r,
            "midpoint_slerp_norm": mid_slerp_norm,
            "midpoint_slerp_ratio": mid_slerp_norm / r,
            "slerp_norm_max_error": slerp_norm_max_err,
            "lerp_midpoint_collapse_sigmas": collapse_in_sigmas,
            "t_values": t_values,
            "lerp_norms": lerp_norms,
            "slerp_norms": slerp_norms,
        }

    def riemannian_brownian_walk(
        self, dim: int, n_steps: int = 500, step_size: float = 0.05
    ) -> Dict[str, Union[float, List[float]]]:
        """
        Executes a stochastic Riemannian random walk on S^{D-1} via:
        1. Ambient Gaussian perturbation w_k ~ N(0, step_size^2 * I)
        2. Projection onto tangent space T_{z_k} S^{D-1}: P_{z_k} w_k
        3. Riemannian exponential map: exp_{z_k}(v_k)
        Proves strict isometric radius conservation at every step.
        """
        r = math.sqrt(dim)
        # Initialize randomly on shell
        z_init = self.sample_gaussian(1, dim)[0]
        z = z_init / np.linalg.norm(z_init) * r

        radii = [float(np.linalg.norm(z))]
        tangent_ortho_errors = []

        for _ in range(n_steps):
            # Ambient perturbation
            w = self.rng.standard_normal(dim) * step_size
            # Tangent projection: v = w - (w . z / ||z||^2) z
            z_norm_sq = float(np.dot(z, z))
            v = w - (np.dot(w, z) / z_norm_sq) * z

            # Check tangent orthogonality
            ortho_dot = abs(float(np.dot(v, z)))
            tangent_ortho_errors.append(ortho_dot)

            # Exponential map: exp_z(v) = cos(||v||/r) z + r sin(||v||/r) (v / ||v||)
            v_norm = float(np.linalg.norm(v))
            if v_norm < 1e-12:
                continue

            phi = v_norm / r
            z = math.cos(phi) * z + r * math.sin(phi) * (v / v_norm)
            radii.append(float(np.linalg.norm(z)))

        radii_arr = np.array(radii)
        max_radius_deviation = float(np.max(np.abs(radii_arr - r)))
        mean_tangent_error = float(np.mean(tangent_ortho_errors))

        return {
            "dim": dim,
            "n_steps": n_steps,
            "shell_radius": r,
            "final_radius": float(radii[-1]),
            "max_radius_deviation": max_radius_deviation,
            "mean_tangent_orthogonality_error": mean_tangent_error,
            "radii_trajectory": radii,
        }


class ActivationDistributionAnalyzer:
    """
    Analyzes neural activation statistics, softmax temperature scaling,
    and classifier-free guidance score flow relaxation.
    """

    def __init__(self, seed: Optional[int] = 42):
        self.rng = np.random.default_rng(seed)

    @staticmethod
    def relu(x: np.ndarray) -> np.ndarray:
        return np.maximum(0.0, x)

    @staticmethod
    def gelu(x: np.ndarray) -> np.ndarray:
        """Gaussian Error Linear Unit (exact CDF formulation)."""
        return 0.5 * x * (1.0 + stats.norm.cdf(x))

    @staticmethod
    def swiglu(x: np.ndarray, gate: np.ndarray) -> np.ndarray:
        """SwiGLU activation: (x * sigmoid(x)) * gate."""
        swish = x / (1.0 + np.exp(-np.clip(x, -30.0, 30.0)))
        return swish * gate

    @staticmethod
    def softmax(logits: np.ndarray, temperature: float = 1.0) -> np.ndarray:
        """Computes numerically stable softmax at given temperature."""
        temp = max(1e-5, temperature)
        scaled = logits / temp
        shifted = scaled - np.max(scaled, axis=-1, keepdims=True)
        exp_vals = np.exp(shifted)
        return exp_vals / np.sum(exp_vals, axis=-1, keepdims=True)

    def analyze_activation_moments(
        self, activation_fn: str, n_samples: int = 10000, dim: int = 512
    ) -> Dict[str, float]:
        """
        Computes statistical moments (mean, variance, skewness, kurtosis, entropy)
        of synthetic pre-activations passed through the specified non-linearity.
        """
        # Standard normal pre-activations
        pre_act = self.rng.standard_normal((n_samples, dim))

        if activation_fn.lower() == "relu":
            acts = self.relu(pre_act)
        elif activation_fn.lower() == "gelu":
            acts = self.gelu(pre_act)
        elif activation_fn.lower() == "swiglu":
            gate = self.rng.standard_normal((n_samples, dim))
            acts = self.swiglu(pre_act, gate)
        else:
            raise ValueError(f"Unknown activation function: {activation_fn}")

        flat = acts.flatten()
        mean_val = float(np.mean(flat))
        var_val = float(np.var(flat, ddof=1))
        skew_val = float(stats.skew(flat))
        kurt_val = float(stats.kurtosis(flat))  # Excess kurtosis (Fisher, normal=0)

        # Fraction of dead/zero activations
        sparsity = float(np.mean(np.abs(flat) < 1e-6))

        return {
            "activation_fn": activation_fn,
            "mean": mean_val,
            "variance": var_val,
            "skewness": skew_val,
            "excess_kurtosis": kurt_val,
            "sparsity": sparsity,
        }

    def analyze_softmax_temperature_entropy(
        self, vocab_size: int = 1000, temperatures: Optional[List[float]] = None
    ) -> Dict[float, Dict[str, float]]:
        """
        Measures Shannon entropy and top-1 probability across temperatures.
        Proves entropy monotonically increases from 0 (argmax) to ln(vocab_size) (uniform).
        """
        if temperatures is None:
            temperatures = [0.05, 0.2, 0.5, 1.0, 2.0, 5.0, 20.0]

        logits = self.rng.standard_normal(vocab_size) * 2.5
        max_entropy = math.log(vocab_size)

        results = {}
        for temp in temperatures:
            probs = self.softmax(logits, temperature=temp)
            # Shannon entropy in nats
            nonzero = probs[probs > 1e-15]
            entropy = float(-np.sum(nonzero * np.log(nonzero)))
            top1_prob = float(np.max(probs))

            results[temp] = {
                "temperature": temp,
                "entropy_nats": entropy,
                "normalized_entropy": entropy / max_entropy,
                "top1_prob": top1_prob,
                "theoretical_max_entropy": max_entropy,
            }
        return results

    def simulate_guidance_relaxation(
        self, dim: int = 128, n_steps: int = 200, guidance_weights: Optional[List[float]] = None
    ) -> Dict[float, Dict[str, float]]:
        """
        Simulates score-based diffusion trajectory under classifier guidance relaxation:
        s_gamma(z) = nabla log p(z) + gamma * nabla log p(y|z)
        where gamma -> 0 represents unconstrained dream flow.
        """
        if guidance_weights is None:
            guidance_weights = [7.5, 3.0, 1.0, 0.2, 0.0]

        # Prior distribution centered at origin
        # Conditional target mode displaced along first coordinate
        target_mode = np.zeros(dim)
        target_mode[0] = 5.0

        results = {}
        for gamma in guidance_weights:
            z = self.rng.standard_normal(dim)
            dt = 0.02
            dispersions = []

            for _ in range(n_steps):
                # Prior score: -z
                prior_score = -z
                # Classifier gradient pulling toward target mode: -(z - target_mode)
                cond_score = -(z - target_mode)
                total_score = prior_score + gamma * cond_score

                # Langevin step
                noise = self.rng.standard_normal(dim) * math.sqrt(2.0 * dt)
                z = z + dt * total_score + noise
                dispersions.append(float(np.linalg.norm(z)))

            final_dist_to_target = float(np.linalg.norm(z - target_mode))
            final_dist_to_prior = float(np.linalg.norm(z))

            results[gamma] = {
                "guidance_weight_gamma": gamma,
                "final_distance_to_conditional_target": final_dist_to_target,
                "final_distance_to_prior_origin": final_dist_to_prior,
                "mean_dispersion": float(np.mean(dispersions)),
                "unconstrained_dream_state": gamma == 0.0,
            }
        return results
