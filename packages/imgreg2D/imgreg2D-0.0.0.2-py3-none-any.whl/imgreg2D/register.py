from datetime import datetime

from imgreg2D import BASE_DIR
from imgreg2D.points import get_registering_points, get_fixed_points, clean_check_points
from imgreg2D.affine import apply_affine, refine_registration, get_affine_matrix
from imgreg2D.utils import load_image, save_warp_matrix, load_warp_matrix




def register(reference, registering, fixed_points=None, warp_mtx=None, save_mtx=False,
                save_fld=None, save_name=None):
    # ------------------------------ Parse arguments ----------------------------- #
    if save_fld is None:
        save_fld = BASE_DIR
    if save_name is None:
        save_name = f"warp_mtx_{datetime.now().strftime('%Y%m%d_%H%M_%S')}"


    if isinstance(reference, str): # images were passed as filepaths
        # Load reference and registering images from file
        reference = load_image(reference)
        registering = load_image(registering)
   
    if warp_mtx is None:
        # Get fixed points, used to compute warp matrix
        if fixed_points is None:
            fixed_points = get_fixed_points(reference)
        else:
            if not isinstance(fixed_points, list):
                fixed_points = [list(p) for p in fixed_points]
            fixed_points = clean_check_points(points=fixed_points, verbose=False)
    else:
        # Load warp matrix from file if necessary
        if isinstance(warp_mtx, str):
            # filepath was passed, load it
            warp_mtx = load_warp_matrix(warp_mtx)
        elif not isinstance(warp_mtx, np.ndarray):
            raise ValueError('The warp matrix argument accepts either paths to .npy files or numpy arrays.'+
                    f"{warp_mtx} was passed?")   
        
        # Check warp matrix shape
        if not warp_mtx.shape == (2, 3):
            raise ValueError("Thw warp matrix has a weird shape"+
                    f"Should be (2, 3) but it is {warp_mtx.shape}.")       

        print("A warp matrix was passed, skipping points extraction.")

    # --------------------------------- Register --------------------------------- #
    happy = False
    while not happy: # keep repeating process until happy
        if warp_mtx is None:
            # Get registration points
            registering_points = get_registering_points(reference, registering, fixed_points)
            warp_mtx = get_affine_matrix(fixed_points, registering_points)

        # Get registered image
        registered = apply_affine(reference, registering, warp_mtx)

        # Visualise results
        happy, warp_mtx, warped_img = refine_registration(reference, registering, registered, warp_mtx)

        # Check if we need to try again
        if happy == 'stop':
            print("\nStopping")
            break
        elif not happy:
            print("\nYou're not happy with the results... trying again!")
            warp_mtx = None
        else:
            print("\nRegistration completed! Saving the results.")
            save_warp_matrix(warp_mtx, save_fld, save_name)

    return warped_img, warp_mtx


