

from __future__ import annotations



import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) #This is so that this file knows the correct path to take, since I put it in a folder.





import re, pickle, requests
from pathlib import Path
from typing import Dict, List, Tuple, Sequence

import numpy as np

from support.constants import BASE_PATH, jacobimin_JPL, jacobimin, mu1, mu2, E0, U_tilde, earth_collision_radius, L2_info
from support.helpers import propagate_orbit, find_all_y0_crossings, crash_surface_vy

# ---------------------------------------------------------------------------
# Constants & API helpers
# ---------------------------------------------------------------------------

_SYSTEM   = "earth-moon"
_BASE_URL = "https://ssd-api.jpl.nasa.gov/periodic_orbits.api"

# Regex for parsing local resonant‑orbit pickle names.  Examples::
#   reso_orbits_31_False.pkl              -> prograde, branch 31
#   reso_orbits_21_1.0_True.pkl           -> retrograde, X:1 ratio (1.0), branch 21
_RE_RESO = re.compile(
    r"^reso_orbits_"
    r"(?P<branch>[0-9]+(?:\.[0-9]+)?)_"   # branch number (e.g. 8 or 8.0)
    r"(?P<ratio>[0-9]+(?:\.[0-9]+)?)_"    # resonance denominator (e.g. 1.0)
    r"retro_(?P<flag>True|False)"          # True → retrograde
    r"\.pkl$",
    re.IGNORECASE)

_FAMILIES_LUNAR: Sequence[Tuple[str, str]] = [  
    ("lyapunov", "Lyapunov"),
    ("dro",       "Distant Retrograde"),
    ("dpo",       "Distant Prograde"),
]
_LPO_BRANCHES_DEFAULT: Sequence[str] = ["E", "W"]

# ---------------------------------------------------------------------------
# Private low‑level helpers
# ---------------------------------------------------------------------------

def _fetch(family: str, jac_min: float, branch: str | None = None) -> np.ndarray:
    """Query the JPL periodic‑orbits API and return raw numpy array data."""
    params = {"sys": _SYSTEM, "family": family, "jacobimin": jac_min}
    if branch is not None:
        params["branch"] = branch

    # Small tweaks to reproduce legacy behaviour exactly
    if family == "lpo" and branch == "W":
        params["jacobimax"] = 3.2
    if family == "dpo":
        params["jacobimin"] = 3.2  # JPL catalogue constraint
    if family == "lyapunov":
        params["libr"] = 1         # restrict to L1 Lyapunov

    try:
        resp = requests.get(_BASE_URL, params=params, timeout=30)
        resp.raise_for_status()
        return np.asarray(resp.json().get("data", []), dtype=float)
    except Exception as exc:  # pragma: no cover – network issues
        print(f"[orbit_data] Warning: API fetch failed for {family}/{branch}: {exc}")
        return np.empty((0,))


def _append_orbits_and_crossings(
    data: np.ndarray,
    label: str,
    *,
    plot_second_crossings: bool,
    out_orbits: List,
    out_cross: List,
    multiple_crossings: bool = False,
    skip_lambda: bool = False,
) -> None:
    """Convert raw state rows into the tuple structure used downstream."""
    if data.size == 0:
        return

    x, vx, vy = data[:, 0], data[:, 3], data[:, 4]
    out_orbits.append((x, vx, vy, label))

    if not plot_second_crossings:
        return

    x2, vx2, vy2 = [], [], []
    for row in data:
        if skip_lambda and row[0] <= 0.85522:  # avoid sensitive LPO segment
            continue
        traj = propagate_orbit(row[:6], row[7])
        crossings = find_all_y0_crossings(traj)
        chosen = crossings if multiple_crossings else crossings[:1]
        for s in chosen:
            if not (label == "LPO W" and s[1] <= 0.85522):  # legacy filter
                x2.append(s[1])
                vx2.append(s[4])
                vy2.append(s[5])

    if x2:
        out_cross.append((np.array(x2), np.array(vx2), np.array(vy2), label))


def _load_crash_ic(pkl_path: Path) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    if not pkl_path.exists():
        return np.array([]), np.array([]), np.array([])
    try:
        with pkl_path.open("rb") as f:
            data = pickle.load(f)
    except Exception as exc:
        print(f"[orbit_data] Warning: could not load crash ICs from '{pkl_path}': {exc}")
        return np.array([]), np.array([]), np.array([])
    if not data:
        return np.array([]), np.array([]), np.array([])
    x0, vx0, vy0 = zip(*data)
    return np.array(x0), np.array(vx0), np.array(vy0)

def _clean(num_str: str) -> str:
    """Remove trailing .0 for integer‑valued floats."""
    if num_str.endswith(".0"):
        return num_str[:-2]
    return num_str

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def gather_analytic_resonant(
    *,
    # Sampling options --------------------------------------------------------
    max_p: int = 20,                  # highest p in the p:1 series (p ≥ 2)
    step_dx: float = 0.01,            # fixed x‑resolution along each line
    x_min: float = 0.08
) -> Dict[str, object]:
    """
    Build an orbit / crossing data set using analytic p:1 resonant seeds.
    The result matches the structure of `gather_dataset`:

        {
            "orbits":    [(x_i, vx_i, vy_i, label), ...],
            "crossings": [(x_c, vx_c, vy_c, label), ...],
            "families_str": "analytic_reso",
        }
    """



    # # -----------------------------------------------------------------------
    # # 0) Pre‑compute envelopes & veto regions on a master x‑grid
    # # -----------------------------------------------------------------------
    # # Choose default x‑range if none given
    
    
    
    
    
    # ######IF I WANT TO REVERT TO THE ORIGINAL, UNCOMMENT THESE TWO LINES INSTEAD OF THE NEXT, CURRENTLY UNCOMMENTED, TWO
    # x_min = -mu2 + earth_collision_radius # Equals 0.006056534599600571 here
    # x_max = L2_info[0][0]
    # # print("JHGIFURDERTUCFYVGIUBHKL", -mu2 + earth_collision_radius)
    ##print("FGIUHLJGKFJDHFJGKH", L2_info[0][0])
    
    
    
    # #######I THINK THIS LETS ME PRINT JUST ONE????? BECAUSE IF THE MIN EQUALS THE MAX THEN IT JUST PRINTS FOR ONE ENERGY LEVEL?????
    # #######NO ITS NOT THE ENERGY LEVEL I DONT THINK!!!!! I THINK IT'S THE STARTING X POSITION FOR THE ORBIT. SO I GUESS EACH OF THE RESONANT ORBITS CAN HAPPEN AT DIFFERENT DISTANCES FROM THE CENTRE MAYBE?????
    # x_min = 0.05
    # x_max = x_min
    
    x_min = x_min
    x_max = x_min

    
    
    # ########JUST TESTING SOME RANGES
    # x_min = 0.36
    # x_max = x_min
    
    # x_min = 0.01
    # x_max = 0.5
    
    # x_min = 0.05
    # x_max = 0.05
    
    # x_min = 0.5
    # x_max = 0.5
    
    
    # x_min = 0.08
    # x_max = 0.08
    
    
    
    # x_min = 0.46
    # x_max = x_min
    
    # x_min = 0.05
    # x_max = 0.07
    
    


    x_full  = np.arange(x_min, x_max + step_dx, step_dx)
    r_plus  = np.abs(x_full + mu2)
    
    
    # accessible‑region envelope   |vy| <= vy_env
    vy_env  = np.sqrt(np.maximum(0.0, 2 * (E0 - U_tilde(x_full, 0.0, mu1, mu2))))
    
    # crash veto
    x_valid, vy_plus, vy_minus = crash_surface_vy(x_full, 0.0, mu1, earth_collision_radius, -mu2)

    # initialise arrays the same length as x_full
    crash_mask = np.zeros_like(x_full,  dtype=bool)
    upper_e    = np.full_like(x_full,   np.nan, dtype=float)
    lower_e    = np.full_like(x_full,   np.nan, dtype=float)


    # map each x_valid to its index in x_full
    # (with fixed step_dx they coincide exactly, else fallback to isclose)
    idx = np.searchsorted(x_full, x_valid)
    # guard against rounding mismatches
    mismatch = ~np.isclose(x_full[idx], x_valid, atol=step_dx*0.1)
    if mismatch.any():                       # rare, but be safe
        idx = np.array([np.where(np.isclose(x_full, xv, atol=step_dx*0.1))[0][0]
                        for xv in x_valid])
    

    

    crash_mask[idx] = True
    upper_e[idx]    = vy_plus
    lower_e[idx]    = vy_minus
    # Containers mimicking gather_dataset output ----------------------------
    all_orbits:    List[Tuple[np.ndarray, np.ndarray, np.ndarray, str]] = []
    all_crossings: List[Tuple[np.ndarray, np.ndarray, np.ndarray, str]] = []

    # -----------------------------------------------------------------------
    # 1) Loop over p and sign (+ → prograde, − → retrograde)
    # -----------------------------------------------------------------------
    for p in range(8, max_p + 1):
        a_p   = (mu1 / p) ** (2 / 3)
        radic = 2 * mu1 * (1.0 / r_plus - 1.0 / (2.0 * a_p))

        # Skip if no real roots anywhere
        base_mask = radic >= 0.0
        if not base_mask.any():
            continue

        for sign in [-1]:#(+1, -1):                      # + = prograde, − = retrograde
            vy_res = sign * np.sqrt(radic[base_mask]) - x_full[base_mask]

            # --- accessible & crash filters --------------------------------
            good_acc = np.abs(vy_res) <= vy_env[base_mask]
            in_crash = (
                crash_mask[base_mask]
                & (vy_res >= lower_e[base_mask])
                & (vy_res <= upper_e[base_mask])
            )
            keep = good_acc & ~in_crash
            if not keep.any():
                continue

            # --- split into contiguous segments so gaps aren’t connected ---
            idx_keep   = np.where(keep)[0]               # indices inside *base_mask*
            split_pts  = np.where(np.diff(idx_keep) > 1)[0] + 1
            segments   = np.split(idx_keep, split_pts)
            # print("EEEEEEEEEEE",segments)

            # === propagate each seed on the master grid ====================
            x_i_list, vx_i_list, vy_i_list = [], [], []
            x_c_list, vx_c_list, vy_c_list = [], [], []
            for seg in segments:
                if seg.size == 0:
                    continue
                # sample every element (already spaced by step_dx)
                for k in seg:
                    x0  = x_full[base_mask][k]
                    vy0 = vy_res[k]
                    state0 = np.array([x0, 0.0, 0.0, 0.0, vy0, 0.0])  # (x,y,z,vx,vy,vz)
                    try:
                        traj = propagate_orbit(state0, period=1.1 * 2 * np.pi)
                    except Exception as exc:
                        print(f"[analytic_reso] propagation failed (p={p}, sign={sign}): {exc}")
                        continue

                    #### print("FFFFFFF",traj.size)
                    
                    # record initial IC
                    x_i_list.append(x0)
                    vx_i_list.append(0.0)
                    vy_i_list.append(vy0)

                    # record *all* y=0 crossings
                    for cross in find_all_y0_crossings(traj):
                        x_c_list.append(cross[1])
                        vx_c_list.append(cross[4])
                        vy_c_list.append(cross[5])


            ###### print("GGGGGGGGG", x_c_list)
            
            
            # Push into gather‑style output lists ---------------------------
            
            if x_i_list:  # nothing appended if list empty
                label_prefix = "Prograde" if sign > 0 else "Retrograde"
                label = f"{label_prefix} {p}:1 analytic"
                all_orbits.append((
                    np.array(x_i_list),
                    np.array(vx_i_list),
                    np.array(vy_i_list),
                    label,
                ))
                if x_c_list:
                    all_crossings.append((
                        np.array(x_c_list),
                        np.array(vx_c_list),
                        np.array(vy_c_list),
                        label,
                    ))
                # print("DDDDDDDDDDDD",x_c_list)
                print(f"[analytic_reso] p={p}: collected {len(x_i_list)} seeds ({label})")

    # -----------------------------------------------------------------------
    # 2) Assemble dict in the same shape as gather_dataset
    # -----------------------------------------------------------------------
    return {
        "orbits":         all_orbits,
        "crossings":      all_crossings,
        "earth_crash_x0": np.array([]),   # none created here
        "earth_crash_vx0": np.array([]),
        "earth_crash_vy0": np.array([]),
        "moon_crash_x0":  np.array([]),
        "moon_crash_vx0": np.array([]),
        "moon_crash_vy0": np.array([]),
        "families_str":   "analytic_reso",
    }
    
    
    
    
    
#####I ADDED THIS ONE
#####DOES THE EXACT SAME THING AS gather_analytic_resonant, JUST FOR A SPECIFIED X VALUE RATHER THAN A RANGE.
#####I COPIED AND PASTED RATHER THAN CHANGE THE OTHER ONE, JUST IN CASE SOME FUNCTION I DONT SEE IS CALLING IT SOMEWHERE AND I NEED TO UPDATE THAT CODE AND STUFF.

#####I SHOULD REALLY CHANGE THIS SO THAT IT DOESNT USE/RETRUN ARRAYS. WE ARE ONLY DOING IT WITH ONE THING NOW, SO IT WILL BE MUCH MORE EFFICIENT TO JUST DO SINGLE VALUES AND NOT WORRY ABOUT ARRAYS. THE ARRAY STUFF IS ALL VESTIGIAL FROM COPY PASTING THE ABOVE.
def gather_analytic_resonant_with_specified_p_and_x_value(
    *,
    # Sampling options --------------------------------------------------------
    max_p: int = 20,                  # highest p in the p:1 series (p ≥ 2)
    # step_dx: float = 0.01,            # fixed x‑resolution along each line
    step_dx: float = 0,            # fixed x‑resolution along each line
    x_value: float = 0.05,            # specified x value
) -> Dict[str, object]:
    """
    Build an orbit / crossing data set using analytic p:1 resonant seeds.
    The result matches the structure of `gather_dataset`:

        {
            "orbits":    [(x_i, vx_i, vy_i, label), ...],
            "crossings": [(x_c, vx_c, vy_c, label), ...],
            "families_str": "analytic_reso",
        }
    """



    # # -----------------------------------------------------------------------
    # # 0) Pre‑compute envelopes & veto regions on a master x‑grid
    # # -----------------------------------------------------------------------
    # # Choose default x‑range if none given
    
    
    
    #######I THINK THIS LETS ME PRINT JUST ONE????? BECAUSE IF THE MIN EQUALS THE MAX THEN IT JUST PRINTS FOR ONE ENERGY LEVEL?????
    #######NO ITS NOT THE ENERGY LEVEL I DONT THINK!!!!! I THINK IT'S THE STARTING X POSITION FOR THE ORBIT. SO I GUESS EACH OF THE RESONANT ORBITS CAN HAPPEN AT DIFFERENT DISTANCES FROM THE CENTRE MAYBE?????
    x_min = x_value
    x_max = x_value
    

    


    # x_full  = np.arange(x_min, x_max + step_dx, step_dx)
    x_full  = np.array([x_value])   ###I JUST CHANGED THE THIS SO THAT IT ONLY CONTAINS THE ONE VALUE, RATHER THAN THE TWO IT WAS DEFAULTING TO BEFORE (CUZ IT AUTOMATICALLY DID UP TO x_max + step_dx)
    r_plus  = np.abs(x_full + mu2)
    
    
    # accessible‑region envelope   |vy| <= vy_env
    vy_env  = np.sqrt(np.maximum(0.0, 2 * (E0 - U_tilde(x_full, 0.0, mu1, mu2))))
    
    # crash veto
    x_valid, vy_plus, vy_minus = crash_surface_vy(x_full, 0.0, mu1, earth_collision_radius, -mu2)

    # initialise arrays the same length as x_full
    crash_mask = np.zeros_like(x_full,  dtype=bool)
    upper_e    = np.full_like(x_full,   np.nan, dtype=float)
    lower_e    = np.full_like(x_full,   np.nan, dtype=float)

    # map each x_valid to its index in x_full
    # (with fixed step_dx they coincide exactly, else fallback to isclose)
    idx = np.searchsorted(x_full, x_valid)
    # guard against rounding mismatches
    mismatch = ~np.isclose(x_full[idx], x_valid, atol=step_dx*0.1)
    if mismatch.any():                       # rare, but be safe
        idx = np.array([np.where(np.isclose(x_full, xv, atol=step_dx*0.1))[0][0]
                        for xv in x_valid])

    crash_mask[idx] = True
    upper_e[idx]    = vy_plus
    lower_e[idx]    = vy_minus
    # Containers mimicking gather_dataset output ----------------------------
    all_orbits:    List[Tuple[np.ndarray, np.ndarray, np.ndarray, str]] = []
    all_crossings: List[Tuple[np.ndarray, np.ndarray, np.ndarray, str]] = []

    # -----------------------------------------------------------------------
    # 1) Loop over p and sign (+ → prograde, − → retrograde)
    # -----------------------------------------------------------------------
    # for p in range(8, max_p + 1):
    
    
    p = max_p ###I HAVE JUST EDITED THE FUNCTION SO IT ONLY DOES IT FOR THE SPECIFIED p VALUE RATHER THAN A RANGE OF p VALUES.
    
    a_p   = (mu1 / p) ** (2 / 3)
    radic = 2 * mu1 * (1.0 / r_plus - 1.0 / (2.0 * a_p))

    # # Skip if no real roots anywhere
    # base_mask = radic >= 0.0
    # if not base_mask.any():
    #     continue
    
    # Skip if no real roots anywhere
    base_mask = radic >= 0.0
    if base_mask.any():
        for sign in [-1]:#(+1, -1):                      # + = prograde, − = retrograde
            vy_res = sign * np.sqrt(radic[base_mask]) - x_full[base_mask]

            # --- accessible & crash filters --------------------------------
            good_acc = np.abs(vy_res) <= vy_env[base_mask]
            in_crash = (
                crash_mask[base_mask]
                & (vy_res >= lower_e[base_mask])
                & (vy_res <= upper_e[base_mask])
            )
            keep = good_acc & ~in_crash
            if not keep.any():
                continue

            # --- split into contiguous segments so gaps aren’t connected ---
            idx_keep   = np.where(keep)[0]               # indices inside *base_mask*
            split_pts  = np.where(np.diff(idx_keep) > 1)[0] + 1
            segments   = np.split(idx_keep, split_pts)

            # === propagate each seed on the master grid ====================
            x_i_list, vx_i_list, vy_i_list = [], [], []
            x_c_list, vx_c_list, vy_c_list = [], [], []
            for seg in segments:
                if seg.size == 0:
                    continue
                # sample every element (already spaced by step_dx)
                for k in seg:
                    x0  = x_full[base_mask][k]
                    vy0 = vy_res[k]
                    state0 = np.array([x0, 0.0, 0.0, 0.0, vy0, 0.0])  # (x,y,z,vx,vy,vz)
                    try:
                        traj = propagate_orbit(state0, period=1.1 * 2 * np.pi)
                    except Exception as exc:
                        print(f"[analytic_reso] propagation failed (p={p}, sign={sign}): {exc}")
                        continue

                    # record initial IC
                    x_i_list.append(x0)
                    vx_i_list.append(0.0)
                    vy_i_list.append(vy0)

                    # record *all* y=0 crossings
                    for cross in find_all_y0_crossings(traj):
                        x_c_list.append(cross[1])
                        vx_c_list.append(cross[4])
                        vy_c_list.append(cross[5])
            
            
            # Push into gather‑style output lists ---------------------------
            
            if x_i_list:  # nothing appended if list empty
                label_prefix = "Prograde" if sign > 0 else "Retrograde"
                label = f"{label_prefix} {p}:1 analytic"
                all_orbits.append((
                    np.array(x_i_list),
                    np.array(vx_i_list),
                    np.array(vy_i_list),
                    label,
                ))
                if x_c_list:
                    all_crossings.append((
                        np.array(x_c_list),
                        np.array(vx_c_list),
                        np.array(vy_c_list),
                        label,
                    ))
                # print("DDDDDDDDDDDD",x_c_list)
                print(f"[analytic_reso] p={p}: collected {len(x_i_list)} seeds ({label})")

    # print("HHHHHHHHHHH", all_orbits)
    # print("IIIIIIIIIIII", all_crossings)

    # -----------------------------------------------------------------------
    # 2) Assemble dict in the same shape as gather_dataset
    # -----------------------------------------------------------------------
    return {
        "orbits":         all_orbits,
        "crossings":      all_crossings,
        "earth_crash_x0": np.array([]),   # none created here
        "earth_crash_vx0": np.array([]),
        "earth_crash_vy0": np.array([]),
        "moon_crash_x0":  np.array([]),
        "moon_crash_vx0": np.array([]),
        "moon_crash_vy0": np.array([]),
        "families_str":   "analytic_reso",
    }







def merge_datasets(dataset1: Dict[str, object], dataset2: Dict[str, object]) -> Dict[str, object]:
    """
    Merge the datasets
    """
    
    merged_orbits = dataset1["orbits"] + dataset2["orbits"]
    merged_crossings = dataset1["crossings"] + dataset2["crossings"]
    merged_families_id = dataset1["families_str"] + dataset2["families_str"]
    # merged_families_id = dataset1["families_str"] #######THIS WAS CAUSING ME A LOT OF PROBLEMS, MAKING THIS WAY TOO LONG WHEN MERGING A LOT OF THINGS, SO LETS JUST CALL IT THE FIRST ONE I GUESS.
    
    return {
        "orbits":         merged_orbits,
        "crossings":      merged_crossings,
        "earth_crash_x0": np.array([]),   # none created here
        "earth_crash_vx0": np.array([]),
        "earth_crash_vy0": np.array([]),
        "moon_crash_x0":  np.array([]),
        "moon_crash_vx0": np.array([]),
        "moon_crash_vy0": np.array([]),
        "families_str":   merged_families_id,
    }



def merge_lists(list1, list2):
        return list1 + list2

