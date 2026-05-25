"""
Sequencing Agent — Arranges tracks into an emotionally intelligent arc.
Creates a journey from current mood → desired emotional state.
"""

from typing import List, Tuple
from models.schemas import Track, MoodAnalysis, Intent, EnergyLevel


# Emotional progression maps: current_mood → arc stages
EMOTIONAL_ARCS = {
    ("tired", "focus"): ["fatigue", "stabilization", "gentle_focus", "deep_concentration"],
    ("anxious", "relax"): ["acknowledgment", "calming", "grounding", "peace"],
    ("sad", "heal"): ["validation", "comfort", "hope", "renewal"],
    ("stressed", "relax"): ["decompression", "calm", "restoration", "tranquility"],
    ("happy", "party"): ["warm_up", "energize", "peak", "sustain"],
    ("energized", "workout"): ["activation", "intensity", "peak", "cooldown"],
    ("neutral", "explore"): ["curiosity", "discovery", "depth", "satisfaction"],
    ("bored", "explore"): ["spark", "momentum", "engagement", "flow"],
    ("melancholic", "heal"): ["empathy", "soothing", "uplift", "release"],
}

# Energy level ordering preferences per arc phase
PHASE_ENERGY_MAP = {
    "fatigue": EnergyLevel.low,
    "stabilization": EnergyLevel.low,
    "gentle_focus": EnergyLevel.medium,
    "deep_concentration": EnergyLevel.medium,
    "acknowledgment": EnergyLevel.low,
    "calming": EnergyLevel.low,
    "grounding": EnergyLevel.low,
    "peace": EnergyLevel.low,
    "validation": EnergyLevel.low,
    "comfort": EnergyLevel.low,
    "hope": EnergyLevel.medium,
    "renewal": EnergyLevel.medium,
    "decompression": EnergyLevel.low,
    "calm": EnergyLevel.low,
    "restoration": EnergyLevel.medium,
    "tranquility": EnergyLevel.low,
    "warm_up": EnergyLevel.medium,
    "energize": EnergyLevel.high,
    "peak": EnergyLevel.high,
    "sustain": EnergyLevel.high,
    "activation": EnergyLevel.medium,
    "intensity": EnergyLevel.high,
    "cooldown": EnergyLevel.medium,
    "curiosity": EnergyLevel.medium,
    "discovery": EnergyLevel.medium,
    "depth": EnergyLevel.medium,
    "satisfaction": EnergyLevel.medium,
    "spark": EnergyLevel.medium,
    "momentum": EnergyLevel.high,
    "engagement": EnergyLevel.high,
    "flow": EnergyLevel.medium,
    "empathy": EnergyLevel.low,
    "soothing": EnergyLevel.low,
    "uplift": EnergyLevel.medium,
    "release": EnergyLevel.medium,
}


def sequence_playlist(
    tracks: List[Track],
    mood: MoodAnalysis,
) -> Tuple[List[Track], List[str]]:
    """
    Arrange tracks into an emotionally progressive order.
    
    Args:
        tracks: Unordered list of recommended tracks
        mood: Current mood analysis
    
    Returns:
        Tuple of (ordered_tracks, emotional_arc_labels)
    """
    # Determine emotional arc
    arc_key = (mood.mood, mood.intent.value)
    arc = EMOTIONAL_ARCS.get(arc_key, ["opening", "middle", "peak", "close"])
    
    # Partition tracks into arc phases
    phase_count = len(arc)
    tracks_per_phase = max(1, len(tracks) // phase_count)
    
    # Sort tracks by energy level to match arc phases
    sorted_by_energy = _sort_by_energy_trajectory(tracks, arc)
    
    # Build final ordered playlist
    ordered: List[Track] = []
    for i, phase in enumerate(arc):
        start = i * tracks_per_phase
        end = start + tracks_per_phase if i < phase_count - 1 else len(sorted_by_energy)
        phase_tracks = sorted_by_energy[start:end]
        ordered.extend(phase_tracks)
    
    return ordered, arc


def _sort_by_energy_trajectory(
    tracks: List[Track],
    arc: List[str],
) -> List[Track]:
    """
    Sort tracks to match the energy trajectory of the emotional arc.
    Assigns energy scores based on arc phase targets.
    """
    energy_order = {EnergyLevel.low: 0, EnergyLevel.medium: 1, EnergyLevel.high: 2, None: 1}
    
    # Compute target energy trajectory
    target_energies = [PHASE_ENERGY_MAP.get(phase, EnergyLevel.medium) for phase in arc]
    
    # Check if arc goes up, down, or peaks
    energy_vals = [energy_order[e] for e in target_energies]
    
    if energy_vals[-1] > energy_vals[0]:
        # Rising arc: sort low → high
        return sorted(tracks, key=lambda t: energy_order.get(t.energy_level, 1))
    elif energy_vals[-1] < energy_vals[0]:
        # Falling arc: sort high → low
        return sorted(tracks, key=lambda t: energy_order.get(t.energy_level, 1), reverse=True)
    else:
        # Peak arc: low → high → low
        low = [t for t in tracks if t.energy_level == EnergyLevel.low]
        mid = [t for t in tracks if t.energy_level == EnergyLevel.medium]
        high = [t for t in tracks if t.energy_level == EnergyLevel.high]
        none = [t for t in tracks if t.energy_level is None]
        
        mid_all = mid + none
        half_low = len(low) // 2
        return low[:half_low] + mid_all[:len(mid_all)//3] + high + mid_all[len(mid_all)//3:] + low[half_low:]


def adapt_sequence_from_behavior(
    current_playlist: List[Track],
    skip_count: int,
    current_index: int,
    skip_pattern: str = "emotional",  # "emotional", "slow", "fast"
) -> List[Track]:
    """
    Adapt playlist in real-time based on skip behavior.
    
    Args:
        current_playlist: Current track list
        skip_count: How many consecutive skips occurred
        current_index: Current position in playlist
        skip_pattern: Detected pattern of what's being skipped
    
    Returns:
        Reordered remaining playlist
    """
    remaining = current_playlist[current_index + 1:]
    
    if skip_pattern == "slow" and skip_count >= 2:
        # User skipping slow songs → surface higher energy tracks
        remaining.sort(key=lambda t: {EnergyLevel.high: 0, EnergyLevel.medium: 1, EnergyLevel.low: 2, None: 1}[t.energy_level])
    
    elif skip_pattern == "fast" and skip_count >= 2:
        # User skipping intense tracks → surface calmer ones
        remaining.sort(key=lambda t: {EnergyLevel.low: 0, EnergyLevel.medium: 1, EnergyLevel.high: 2, None: 1}[t.energy_level])
    
    elif skip_pattern == "emotional" and skip_count >= 3:
        # User skipping emotional tracks → push instrumentals first
        instrumental_keywords = ["instrumental", "ambient", "lo-fi", "lofi", "piano", "study"]
        def is_instrumental(t: Track) -> bool:
            combined = (t.title + " " + t.artist).lower()
            return any(kw in combined for kw in instrumental_keywords)
        
        instrumentals = [t for t in remaining if is_instrumental(t)]
        others = [t for t in remaining if not is_instrumental(t)]
        remaining = instrumentals + others
    
    return current_playlist[:current_index + 1] + remaining