#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 10:40:07 2017
Copyright (C) 2017
@author: Derek Pisner
"""
import os
import nibabel as nib
import warnings
import numpy as np
from pynets.registration import reg_utils as regutils
from nilearn.image import math_img
warnings.filterwarnings("ignore")
try:
    FSLDIR = os.environ['FSLDIR']
except KeyError:
    print('FSLDIR environment variable not set!')


def direct_streamline_norm(streams, fa_path, ap_path, dir_path, track_type, target_samples, conn_model, network,
                           node_size, dens_thresh, ID, roi, min_span_tree, disp_filt, parc, prune, atlas,
                           labels_im_file, uatlas, labels, coords, norm, binary, atlas_mni, basedir_path,
                           curv_thr_list, step_list, directget, min_length, error_margin):
    """
    A Function to perform normalization of streamlines tracked in native diffusion space to an
    FA template in MNI space.

    Parameters
    ----------
    streams : str
        File path to save streamline array sequence in .trk format.
    fa_path : str
        File path to FA Nifti1Image.
    ap_path : str
        File path to the anisotropic power Nifti1Image.
    dir_path : str
        Path to directory containing subject derivative data for a given pynets run.
    track_type : str
        Tracking algorithm used (e.g. 'local' or 'particle').
    target_samples : int
        Total number of streamline samples specified to generate streams.
    conn_model : str
        Connectivity reconstruction method (e.g. 'csa', 'tensor', 'csd').
    network : str
        Resting-state network based on Yeo-7 and Yeo-17 naming (e.g. 'Default')
        used to filter nodes in the study of brain subgraphs.
    node_size : int
        Spherical centroid node size in the case that coordinate-based centroids
        are used as ROI's for tracking.
    dens_thresh : bool
        Indicates whether a target graph density is to be used as the basis for
        thresholding.
    ID : str
        A subject id or other unique identifier.
    roi : str
        File path to binarized/boolean region-of-interest Nifti1Image file.
    min_span_tree : bool
        Indicates whether local thresholding from the Minimum Spanning Tree
        should be used.
    disp_filt : bool
        Indicates whether local thresholding using a disparity filter and
        'backbone network' should be used.
    parc : bool
        Indicates whether to use parcels instead of coordinates as ROI nodes.
    prune : bool
        Indicates whether to prune final graph of disconnected nodes/isolates.
    atlas : str
        Name of atlas parcellation used.
    labels_im_file : str
        File path to atlas parcellation Nifti1Image aligned to dwi space.
    uatlas : str
        File path to atlas parcellation Nifti1Image in MNI template space.
    labels : list
        List of string labels corresponding to graph nodes.
    coords : list
        List of (x, y, z) tuples corresponding to a coordinate atlas used or
        which represent the center-of-mass of each parcellation node.
    norm : int
        Indicates method of normalizing resulting graph.
    binary : bool
        Indicates whether to binarize resulting graph edges to form an
        unweighted graph.
    atlas_mni : str
        File path to atlas parcellation Nifti1Image in T1w-warped MNI space.
    basedir_path : str
        Path to directory to output direct-streamline normalized temp files and outputs.
    curv_thr_list : list
        List of integer curvature thresholds used to perform ensemble tracking.
    step_list : list
        List of float step-sizes used to perform ensemble tracking.
    directget : str
        The statistical approach to tracking. Options are: det (deterministic),
        closest (clos), boot (bootstrapped), and prob (probabilistic).
    min_length : int
        Minimum fiber length threshold in mm to restrict tracking.
    error_margin : int
        Distance (in the units of the streamlines, usually mm). If any
        coordinate in the streamline is within this distance from the center
        of any voxel in the ROI, the filtering criterion is set to True for
        this streamline, otherwise False. Defaults to the distance between
        the center of each voxel and the corner of the voxel.

    Returns
    -------
    streams_warp : str
        File path to normalized streamline array sequence in .trk format.
    dir_path : str
        Path to directory containing subject derivative data for a given pynets run.
    track_type : str
        Tracking algorithm used (e.g. 'local' or 'particle').
    target_samples : int
        Total number of streamline samples specified to generate streams.
    conn_model : str
        Connectivity reconstruction method (e.g. 'csa', 'tensor', 'csd').
    network : str
        Resting-state network based on Yeo-7 and Yeo-17 naming (e.g. 'Default')
        used to filter nodes in the study of brain subgraphs.
    node_size : int
        Spherical centroid node size in the case that coordinate-based centroids
        are used as ROI's for tracking.
    dens_thresh : bool
        Indicates whether a target graph density is to be used as the basis for
        thresholding.
    ID : str
        A subject id or other unique identifier.
    roi : str
        File path to binarized/boolean region-of-interest Nifti1Image file.
    min_span_tree : bool
        Indicates whether local thresholding from the Minimum Spanning Tree
        should be used.
    disp_filt : bool
        Indicates whether local thresholding using a disparity filter and
        'backbone network' should be used.
    parc : bool
        Indicates whether to use parcels instead of coordinates as ROI nodes.
    prune : bool
        Indicates whether to prune final graph of disconnected nodes/isolates.
    atlas : str
        Name of atlas parcellation used.
    uatlas : str
        File path to atlas parcellation Nifti1Image in MNI template space.
    labels : list
        List of string labels corresponding to graph nodes.
    coords : list
        List of (x, y, z) tuples corresponding to a coordinate atlas used or
        which represent the center-of-mass of each parcellation node.
    norm : int
        Indicates method of normalizing resulting graph.
    binary : bool
        Indicates whether to binarize resulting graph edges to form an
        unweighted graph.
    atlas_mni : str
        File path to atlas parcellation Nifti1Image in T1w-warped MNI space.
    directget : str
        The statistical approach to tracking. Options are: det (deterministic), closest (clos), boot (bootstrapped),
        and prob (probabilistic).
    warped_fa : str
        File path to MNI-space warped FA Nifti1Image.
    min_length : int
        Minimum fiber length threshold in mm to restrict tracking.
    error_margin : int
        Distance (in the units of the streamlines, usually mm). If any
        coordinate in the streamline is within this distance from the center
        of any voxel in the ROI, the filtering criterion is set to True for
        this streamline, otherwise False. Defaults to the distance between
        the center of each voxel and the corner of the voxel.
    References
    ----------
    .. [1] Greene, C., Cieslak, M., & Grafton, S. T. (2017). Effect of different spatial normalization approaches on
           tractography and structural brain networks. Network Neuroscience, 1-19.
    """
    import gc
    from dipy.tracking import utils
    from dipy.tracking.streamline import values_from_volume, transform_streamlines, Streamlines
    from pynets.registration import reg_utils as regutils
    from dipy.tracking._utils import _mapping_to_voxel
    from dipy.io.stateful_tractogram import Space, StatefulTractogram, Origin
    from dipy.io.streamline import save_tractogram
    # from pynets.plotting import plot_gen
    import pkg_resources
    import os.path as op
    from nilearn.image import resample_to_img
    from dipy.io.streamline import load_tractogram

    dsn_dir = "%s%s" % (basedir_path, '/dmri_reg_tmp/DSN')
    if not op.isdir(dsn_dir):
        os.mkdir(dsn_dir)

    namer_dir = '{}/tractography'.format(dir_path)
    if not op.isdir(namer_dir):
        os.mkdir(namer_dir)

    atlas_img = nib.load(labels_im_file)

    # Run SyN and normalize streamlines
    fa_img = nib.load(fa_path)
    vox_size = fa_img.header.get_zooms()[0]
    template_path = pkg_resources.resource_filename("pynets", "%s%s%s" % ('templates/FA_', int(vox_size), 'mm.nii.gz'))
    template_anat_path = pkg_resources.resource_filename("pynets", "%s%s%s" % ('templates/MNI152_T1_', int(vox_size),
                                                                               'mm_brain.nii.gz'))
    template_img = nib.load(template_path)
    brain_mask = np.asarray(template_img.dataobj).astype('bool')
    template_img.uncache()

    streams_mni = "%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s" % (namer_dir, '/streamlines_mni_',
                                                              '%s' % (network + '_' if network is not
                                                                                       None else ''),
                                                              '%s' % (op.basename(roi).split('.')[0] + '_'
                                                                      if roi is not None else ''),
                                                              conn_model, '_', target_samples,
                                                              '%s' % ("%s%s" % ('_' +
                                                                                str(node_size), 'mm_') if
                                                                      ((node_size != 'parc') and
                                                                       (node_size is not None)) else '_'),
                                                              'curv', str(curv_thr_list).replace(', ', '_'),
                                                              'step', str(step_list).replace(', ', '_'),
                                                              'tt-', track_type, '_dg-', directget, '_ml-',
                                                              min_length, '.trk')

    density_mni = "%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s" % (namer_dir, '/density_map_mni_',
                                                              '%s' % (network + '_' if network is not None else ''),
                                                              '%s' % (op.basename(roi).split('.')[0] + '_' if
                                                                      roi is not None else ''),
                                                              conn_model, '_', target_samples,
                                                              '%s' % ("%s%s" % ('_' + str(node_size), 'mm_') if
                                                                      ((node_size != 'parc') and (node_size is not
                                                                                                  None)) else '_'),
                                                              'curv', str(curv_thr_list).replace(', ', '_'),
                                                              'step', str(step_list).replace(', ', '_'), 'tt-',
                                                              track_type,
                                                              '_dg-', directget, '_ml-', min_length, '.nii.gz')

    # streams_warp_png = "%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s" % (dsn_dir, '/streamlines_mni_warp_',
    #                                                                '%s' % (network + '_' if network is not
    #                                                                                         None else ''),
    #                                                                '%s' % (op.basename(roi).split('.')[0] + '_' if
    #                                                                        roi is not None else ''),
    #                                                                conn_model, '_', target_samples,
    #                                                                '%s' % ("%s%s" %
    #                                                                        ('_' + str(node_size),
    #                                                                         'mm_') if ((node_size != 'parc') and
    #                                                                                    (node_size is not None)) else
    #                                                                        '_'),
    #                                                                'curv', str(curv_thr_list).replace(', ', '_'),
    #                                                                'step', str(step_list).replace(', ', '_'), 'tt-',
    #                                                                track_type,  '_dg-', directget, '_ml-', min_length,
    #                                                                '.png')

    # SyN FA->Template
    [mapping, affine_map, warped_fa] = regutils.wm_syn(template_path, fa_path, template_anat_path, ap_path, dsn_dir)

    tractogram = load_tractogram(streams, fa_img, to_space=Space.RASMM, to_origin=Origin.TRACKVIS,
                                 bbox_valid_check=False)
    fa_img.uncache()
    streamlines = tractogram.streamlines
    warped_fa_img = nib.load(warped_fa)
    warped_fa_affine = warped_fa_img.affine
    warped_fa_shape = warped_fa_img.shape

    streams_in_curr_grid = transform_streamlines(streamlines, warped_fa_affine)

    ref_grid_aff = vox_size*np.eye(4)
    ref_grid_aff[3][3] = 1

    # Create isocenter mapping where we anchor the origin transformation affine
    # to the corner of the FOV by scaling x, y, z offsets according to a multiplicative
    # van der Corput sequence with a base value equal to the voxel resolution
    def vdc(n, base=vox_size):
        vdc, denom = 0, 1
        while n:
            denom *= base
            n, remainder = divmod(n, base)
            vdc += remainder / denom
        return vdc

    [x_mul, y_mul, z_mul] = [vdc(i) for i in range(1, 4)]

    adjusted_affine = affine_map.affine.copy()
    adjusted_affine[0][3] = -adjusted_affine[0][3]*x_mul
    adjusted_affine[1][3] = -adjusted_affine[1][3]*y_mul
    adjusted_affine[2][3] = -adjusted_affine[2][3]*z_mul

    # Deform streamlines, isocenter, and remove streamlines outside brain
    streams_final_filt = Streamlines(utils.target_line_based(
        transform_streamlines(transform_streamlines(
            [sum(d, s) for d, s in zip(values_from_volume(mapping.get_forward_field(), streams_in_curr_grid,
                                                          ref_grid_aff), streams_in_curr_grid)],
            np.linalg.inv(adjusted_affine)), np.linalg.inv(warped_fa_img.affine)), np.eye(4), brain_mask,
        include=True))

    # Remove streamlines with negative voxel indices
    lin_T, offset = _mapping_to_voxel(np.eye(4))
    streams_final_filt_final = []
    for sl in streams_final_filt:
        inds = np.dot(sl, lin_T)
        inds += offset
        if not inds.min().round(decimals=6) < 0:
            streams_final_filt_final.append(sl)

    # Save streamlines
    stf = StatefulTractogram(streams_final_filt_final, reference=warped_fa_img, space=Space.RASMM,
                             origin=Origin.TRACKVIS)
    stf.remove_invalid_streamlines()
    streams_final_filt_final = stf.streamlines
    save_tractogram(stf, streams_mni, bbox_valid_check=True)
    warped_fa_img.uncache()

    # DSN QC plotting
    # plot_gen.show_template_bundles(streams_final_filt_final, template_path, streams_warp_png)

    # Create and save MNI density map
    nib.save(nib.Nifti1Image(utils.density_map(streams_final_filt_final, affine=np.eye(4),
                                               vol_dims=warped_fa_shape), warped_fa_affine), density_mni)

    # Map parcellation from native space back to MNI-space and create an 'uncertainty-union' parcellation
    # with original mni-space uatlas
    uatlas_mni_img = nib.load(uatlas)

    warped_uatlas = affine_map.transform_inverse(mapping.transform(np.asarray(atlas_img.dataobj).astype('int'),
                                                                   interpolation='nearestneighbour'), interp='nearest')
    atlas_img.uncache()
    warped_uatlas_img_res_data = np.asarray(resample_to_img(nib.Nifti1Image(warped_uatlas, affine=warped_fa_affine),
                                                            uatlas_mni_img, interpolation='nearest',
                                                            clip=False).dataobj)
    uatlas_mni_data = np.asarray(uatlas_mni_img.dataobj)
    uatlas_mni_img.uncache()
    overlap_mask = np.invert(warped_uatlas_img_res_data.astype('bool') * uatlas_mni_data.astype('bool'))
    atlas_mni = "%s%s%s%s" % (dir_path, '/parcellations/', op.basename(uatlas).split('.nii')[0],
                              '_UNION.nii.gz')
    nib.save(nib.Nifti1Image(warped_uatlas_img_res_data * overlap_mask.astype('int') +
                             uatlas_mni_data * overlap_mask.astype('int') +
                             np.invert(overlap_mask).astype('int') *
                             warped_uatlas_img_res_data, affine=warped_fa_affine), atlas_mni)

    del (tractogram, streamlines, warped_uatlas_img_res_data, uatlas_mni_data, overlap_mask, stf,
         streams_final_filt_final, streams_final_filt, streams_in_curr_grid, brain_mask)

    gc.collect()

    return (streams_mni, dir_path, track_type, target_samples, conn_model, network, node_size, dens_thresh, ID, roi,
            min_span_tree, disp_filt, parc, prune, atlas, uatlas, labels, coords, norm, binary, atlas_mni, directget,
            warped_fa, min_length, error_margin)


class DmriReg(object):
    """
    A Class for Registering an atlas to a subject's MNI-aligned T1w image in native diffusion space.
    """

    def __init__(self, basedir_path, fa_path, ap_path, B0_mask, anat_file, mask, vox_size, simple):
        import pkg_resources
        import os.path as op
        self.simple = simple
        self.ap_path = ap_path
        self.fa_path = fa_path
        self.B0_mask = B0_mask
        self.t1w = anat_file
        self.mask = mask
        self.vox_size = vox_size
        self.t1w_name = 't1w'
        self.dwi_name = 'dwi'
        self.basedir_path = basedir_path
        self.tmp_path = "%s%s" % (basedir_path, '/dmri_reg_tmp')
        self.reg_path = "%s%s" % (basedir_path, '/dmri_reg_tmp/reg')
        self.anat_path = "%s%s" % (basedir_path, '/anat_reg')
        self.reg_path_mat = "%s%s" % (self.reg_path, '/mats')
        self.reg_path_warp = "%s%s" % (self.reg_path, '/warps')
        self.reg_path_img = "%s%s" % (self.reg_path, '/imgs')
        self.t12mni_xfm_init = "%s%s" % (self.reg_path_mat, "/xfm_t1w2mni_init.mat")
        self.mni2t1_xfm_init = "%s%s" % (self.reg_path_mat, "/xfm_mni2t1w_init.mat")
        self.t12mni_xfm = "%s%s" % (self.reg_path_mat, "/xfm_t1w2mni.mat")
        self.mni2t1_xfm = "%s%s" % (self.reg_path_mat, "/xfm_mni2t1.mat")
        self.mni2t1w_warp = "%s%s" % (self.reg_path_warp, "/mni2t1w_warp.nii.gz")
        self.warp_t1w2mni = "%s%s" % (self.reg_path_warp, "/t1w2mni_warp.nii.gz")
        self.t1w2dwi = "%s%s%s%s" % (self.reg_path_img, '/', self.t1w_name, "_in_dwi.nii.gz")
        self.t1_aligned_mni = "%s%s%s%s" % (self.anat_path, '/', self.t1w_name, "_aligned_mni.nii.gz")
        self.t1w_brain = "%s%s%s%s" % (self.anat_path, '/', self.t1w_name, "_brain.nii.gz")
        self.t1w_brain_mask = "%s%s%s%s" % (self.anat_path, '/', self.t1w_name, "_brain_mask.nii.gz")
        self.dwi2t1w_xfm = "%s%s" % (self.reg_path_mat, "/dwi2t1w_xfm.mat")
        self.t1w2dwi_xfm = "%s%s" % (self.reg_path_mat, "/t1w2dwi_xfm.mat")
        self.t1w2dwi_bbr_xfm = "%s%s" % (self.reg_path_mat, "/t1w2dwi_bbr_xfm.mat")
        self.dwi2t1w_bbr_xfm = "%s%s" % (self.reg_path_mat, "/dwi2t1w_bbr_xfm.mat")
        self.t1wtissue2dwi_xfm = "%s%s" % (self.reg_path_mat, "/t1wtissue2dwi_xfm.mat")
        self.xfm_atlas2t1w_init = "%s%s%s%s" % (self.reg_path_mat, '/', self.t1w_name, "_xfm_atlas2t1w_init.mat")
        self.atlas2t1mni_xfm_init = "%s%s%s%s" % (self.reg_path_mat, '/', self.t1w_name, "_xfm_atlas2t1mni_init.mat")
        self.xfm_atlas2t1w = "%s%s%s%s" % (self.reg_path_mat, '/', self.t1w_name, "_xfm_atlas2t1w.mat")
        self.atlas_skull2dwi_xfm = "%s%s" % (self.reg_path_mat, "/atlas_skull2dwi_xfm.mat")
        self.temp2dwi_xfm = "%s%s%s%s" % (self.reg_path_mat, '/', self.dwi_name, "_xfm_temp2dwi.mat")
        self.temp2dwi_xfm = "%s%s%s%s" % (self.reg_path_mat, '/', self.dwi_name, "_xfm_temp2dwi.mat")
        self.map_path = "%s%s%s%s" % (self.anat_path, '/', self.t1w_name, "_seg")
        self.wm_mask = "%s%s%s%s" % (self.anat_path, '/', self.t1w_name, "_wm.nii.gz")
        self.wm_mask_thr = "%s%s%s%s" % (self.anat_path, '/', self.t1w_name, "_wm_thr.nii.gz")
        self.wm_edge = "%s%s%s%s" % (self.anat_path, '/', self.t1w_name, "_wm_edge.nii.gz")
        self.csf_mask = "%s%s%s%s" % (self.anat_path, '/', self.t1w_name, "_csf.nii.gz")
        self.gm_mask = "%s%s%s%s" % (self.anat_path, '/', self.t1w_name, "_gm.nii.gz")
        self.xfm_roi2mni_init = "%s%s" % (self.reg_path_mat, "/roi_2_mni.mat")
        self.mni_vent_loc = pkg_resources.resource_filename("pynets", "templates/LateralVentricles_" + vox_size +
                                                            ".nii.gz")
        self.csf_mask_dwi = "%s%s%s%s" % (self.reg_path_img, '/', self.t1w_name, "_csf_mask_dwi.nii.gz")
        self.gm_in_dwi = "%s%s%s%s" % (self.reg_path_img, '/', self.t1w_name, "_gm_in_dwi.nii.gz")
        self.wm_in_dwi = "%s%s%s%s" % (self.reg_path_img, '/', self.t1w_name, "_wm_in_dwi.nii.gz")
        self.csf_mask_dwi_bin = "%s%s%s%s" % (self.reg_path_img, '/', self.t1w_name, "_csf_mask_dwi_bin.nii.gz")
        self.gm_in_dwi_bin = "%s%s%s%s" % (self.reg_path_img, '/', self.t1w_name, "_gm_in_dwi_bin.nii.gz")
        self.wm_in_dwi_bin = "%s%s%s%s" % (self.reg_path_img, '/', self.t1w_name, "_wm_in_dwi_bin.nii.gz")
        self.vent_mask_dwi = "%s%s%s%s" % (self.reg_path_img, '/', self.t1w_name, "_vent_mask_dwi.nii.gz")
        self.vent_csf_in_dwi = "%s%s%s%s" % (self.reg_path_img, '/', self.t1w_name, "_vent_csf_in_dwi.nii.gz")
        self.vent_mask_mni = "%s%s" % (self.reg_path_img, "/vent_mask_mni.nii.gz")
        self.vent_mask_t1w = "%s%s" % (self.reg_path_img, "/vent_mask_t1w.nii.gz")
        self.input_mni = pkg_resources.resource_filename("pynets", "templates/MNI152_T1_" + vox_size + ".nii.gz")
        self.input_mni_brain = pkg_resources.resource_filename("pynets", "templates/MNI152_T1_" + vox_size +
                                                               "_brain.nii.gz")
        self.input_mni_mask = pkg_resources.resource_filename("pynets", "templates/MNI152_T1_" + vox_size +
                                                              "_brain_mask.nii.gz")
        self.mni_atlas = pkg_resources.resource_filename("pynets", "core/atlases/HarvardOxford-sub-prob-" + vox_size +
                                                         ".nii.gz")
        self.wm_gm_int_in_dwi = "%s%s%s%s" % (self.reg_path_img, '/', self.t1w_name, "_wm_gm_int_in_dwi.nii.gz")
        self.wm_gm_int_in_dwi_bin = "%s%s%s%s" % (self.reg_path_img, '/', self.t1w_name,
                                                  "_wm_gm_int_in_dwi_bin.nii.gz")
        self.corpuscallosum = pkg_resources.resource_filename("pynets", "templates/CorpusCallosum_" + vox_size +
                                                              ".nii.gz")
        self.corpuscallosum_mask_t1w = ("%s%s" % (self.reg_path_img, '/CorpusCallosum_t1wmask.nii.gz'))
        self.corpuscallosum_dwi = ("%s%s" % (self.reg_path_img, '/CorpusCallosum_dwi.nii.gz'))
        self.waymask_in_t1w = "%s%s" % (self.reg_path_img, '/waymask_in_t1w.nii.gz')
        self.waymask_in_dwi = "%s%s" % (self.reg_path_img, '/waymask_in_dwi.nii.gz')

        # Create empty tmp directories that do not yet exist
        reg_dirs = [self.tmp_path, self.reg_path, self.anat_path, self.reg_path_mat, self.reg_path_warp,
                    self.reg_path_img]
        for i in range(len(reg_dirs)):
            if not op.isdir(reg_dirs[i]):
                os.mkdir(reg_dirs[i])

        if op.isfile(self.t1w_brain) is False:
            import shutil
            shutil.copyfile(self.t1w, self.t1w_brain)

    def gen_tissue(self, overwrite=True):
        """
        A function to segment and threshold tissue types from T1w.
        """
        # from pynets.plotting.plot_gen import qa_fast_png
        import os.path as op
        import glob
        import shutil

        # Apply brain mask if detected as a separate file
        try:
            anat_mask_existing = glob.glob(op.dirname(self.t1w) + '/*_desc-brain_mask.nii.gz')[0]
            if op.isfile(anat_mask_existing) and not self.mask and overwrite is False:
                anat_mask_existing = regutils.check_orient_and_dims(anat_mask_existing, self.basedir_path,
                                                                    self.vox_size)
                try:
                    os.system("fslmaths {} -mas {} {} 2>/dev/null".format(self.t1w_brain, anat_mask_existing,
                                                                          self.t1w_brain))
                except:
                    try:
                        from nilearn.image import resample_to_img
                        nib.save(resample_to_img(nib.load(anat_mask_existing), nib.load(self.t1w_brain)),
                                 anat_mask_existing)
                        os.system("fslmaths {} -mas {} {} 2>/dev/null".format(self.t1w_brain, anat_mask_existing,
                                                                              self.t1w_brain))
                    except ValueError:
                        print('Cannot coerce mask to shape of T1w anatomical.')

            # Segment the t1w brain into probability maps
            gm_mask_existing = glob.glob(op.dirname(self.t1w) + '/*_label-GM_probseg.nii.gz')[0]
            wm_mask_existing = glob.glob(op.dirname(self.t1w) + '/*_label-WM_probseg.nii.gz')[0]
            csf_mask_existing = glob.glob(op.dirname(self.t1w) + '/*_label-CSF_probseg.nii.gz')[0]
        except:
            anat_mask_existing = None
            wm_mask_existing = None
            gm_mask_existing = None
            csf_mask_existing = None

        if wm_mask_existing and gm_mask_existing and csf_mask_existing and overwrite is False:
            if op.isfile(wm_mask_existing) and op.isfile(gm_mask_existing) and op.isfile(csf_mask_existing):
                wm_mask = regutils.check_orient_and_dims(wm_mask_existing, self.basedir_path,
                                                         self.vox_size, overwrite=False)
                gm_mask = regutils.check_orient_and_dims(gm_mask_existing, self.basedir_path,
                                                         self.vox_size, overwrite=False)
                csf_mask = regutils.check_orient_and_dims(csf_mask_existing, self.basedir_path,
                                                          self.vox_size, overwrite=False)
            else:
                try:
                    maps = regutils.segment_t1w(self.t1w_brain, self.map_path)
                except RuntimeError:
                    print('Segmentation failed. Does the input anatomical image still contained skull?')
                wm_mask = maps['wm_prob']
                gm_mask = maps['gm_prob']
                csf_mask = maps['csf_prob']
        else:
            try:
                maps = regutils.segment_t1w(self.t1w_brain, self.map_path)
            except RuntimeError:
                print('Segmentation failed. Does the input anatomical image still contained skull?')
            wm_mask = maps['wm_prob']
            gm_mask = maps['gm_prob']
            csf_mask = maps['csf_prob']

        # qa_fast_png(self.csf_mask, self.gm_mask, self.wm_mask, self.map_path)

        # Threshold WM to binary in dwi space
        t_img = nib.load(wm_mask)
        mask = math_img('img > 0.20', img=t_img)
        mask.to_filename(self.wm_mask_thr)

        # Threshold T1w brain to binary in anat space
        t_img = nib.load(self.t1w_brain)
        mask = math_img('img > 0.0', img=t_img)
        mask.to_filename(self.t1w_brain_mask)

        # Extract wm edge
        os.system("fslmaths {} -edge -bin -mas {} {} 2>/dev/null".format(wm_mask, self.wm_mask_thr,
                                                                         self.wm_edge))

        shutil.copyfile(wm_mask, self.wm_mask)
        shutil.copyfile(gm_mask, self.gm_mask)
        shutil.copyfile(csf_mask, self.csf_mask)

        return

    def t1w2dwi_align(self):
        """
        A function to perform alignment from T1w --> MNI and T1w_MNI --> DWI. Uses a local optimisation
        cost function to get the two images close, and then uses bbr to obtain a good alignment of brain boundaries.
        Assumes input dwi is already preprocessed and brain extracted.
        """

        # Create linear transform/ initializer T1w-->MNI
        regutils.align(self.t1w_brain, self.input_mni_brain, xfm=self.t12mni_xfm_init, bins=None, interp="spline",
                       out=None, dof=12, cost='mutualinfo', searchrad=True)

        # Attempt non-linear registration of T1 to MNI template
        if self.simple is False:
            try:
                print('Running non-linear registration: T1w-->MNI ...')
                # Use FNIRT to nonlinearly align T1 to MNI template
                regutils.align_nonlinear(self.t1w_brain, self.input_mni, xfm=self.t12mni_xfm_init,
                                         out=self.t1_aligned_mni, warp=self.warp_t1w2mni, ref_mask=self.input_mni_mask)

                # Get warp from MNI -> T1
                regutils.inverse_warp(self.t1w_brain, self.mni2t1w_warp, self.warp_t1w2mni)

                # Get mat from MNI -> T1
                os.system("convert_xfm -omat {} -inverse {} 2>/dev/null".format(self.mni2t1_xfm_init,
                                                                                self.t12mni_xfm_init))

            except RuntimeError('Error: FNIRT failed!'):
                pass
        else:
            # Falling back to linear registration
            regutils.align(self.t1w_brain, self.input_mni_brain, xfm=self.t12mni_xfm, init=self.t12mni_xfm_init,
                           bins=None, dof=12, cost='mutualinfo', searchrad=True, interp="spline",
                           out=self.t1_aligned_mni, sch=None)
            # Get mat from MNI -> T1
            os.system("convert_xfm -omat {} -inverse {} 2>/dev/null".format(self.t12mni_xfm, self.mni2t1_xfm))

        # Align T1w-->DWI
        regutils.align(self.ap_path, self.t1w_brain, xfm=self.t1w2dwi_xfm, bins=None, interp="spline", dof=6,
                       cost='mutualinfo', out=None, searchrad=True, sch=None)
        os.system("convert_xfm -omat {} -inverse {} 2>/dev/null".format(self.dwi2t1w_xfm, self.t1w2dwi_xfm))

        if self.simple is False:
            # Flirt bbr
            try:
                print('Running FLIRT BBR registration: T1w-->DWI ...')
                regutils.align(self.fa_path, self.t1w_brain, wmseg=self.wm_edge, xfm=self.dwi2t1w_bbr_xfm,
                               init=self.dwi2t1w_xfm, bins=256, dof=7, searchrad=True, interp="spline", out=None,
                               cost='bbr', sch="${FSLDIR}/etc/flirtsch/bbr.sch")
                os.system("convert_xfm -omat {} -inverse {} 2>/dev/null".format(self.t1w2dwi_bbr_xfm,
                                                                                self.dwi2t1w_bbr_xfm))

                # Apply the alignment
                regutils.align(self.t1w_brain, self.ap_path, init=self.t1w2dwi_bbr_xfm, xfm=self.t1wtissue2dwi_xfm,
                               bins=None, interp="spline", dof=7, cost='mutualinfo', out=self.t1w2dwi, searchrad=True,
                               sch=None)
            except RuntimeError('Error: FLIRT BBR failed!'):
                pass
        else:
            # Apply the alignment
            regutils.align(self.t1w_brain, self.ap_path, init=self.t1w2dwi_xfm, xfm=self.t1wtissue2dwi_xfm, bins=None,
                           interp="spline", dof=6, cost='mutualinfo', out=self.t1w2dwi, searchrad=True, sch=None)

        return

    def atlas2t1w2dwi_align(self, uatlas, uatlas_parcels, atlas):
        """
        A function to perform atlas alignment atlas --> T1 --> dwi.
        Tries nonlinear registration first, and if that fails, does a linear registration instead. For this to succeed,
        must first have called t1w2dwi_align.
        """
        aligned_atlas_t1mni = "%s%s%s%s" % (self.anat_path, '/', atlas, "_t1w_mni.nii.gz")
        aligned_atlas_skull = "%s%s%s%s" % (self.anat_path, '/', atlas, "_t1w_skull.nii.gz")
        dwi_aligned_atlas = "%s%s%s%s" % (self.reg_path_img, '/', atlas, "_dwi_track.nii.gz")
        dwi_aligned_atlas_wmgm_int = "%s%s%s%s" % (self.reg_path_img, '/', atlas, "_dwi_track_wmgm_int.nii.gz")
        uatlas_filled = "%s%s%s%s" % (self.reg_path_img, '/', atlas, "_filled.nii.gz")

        os.system("fslmaths {} -add {} -mas {} {} 2>/dev/null".format(self.input_mni_brain, uatlas,
                                                                      self.input_mni_mask, uatlas_filled))

        regutils.align(uatlas_filled, self.t1_aligned_mni, init=None, xfm=self.atlas2t1mni_xfm_init,
                       out=None, dof=12, searchrad=True, interp="nearestneighbour", cost='mutualinfo')

        if self.simple is False:
            try:
                # Apply warp resulting from the inverse of T1w-->MNI created earlier
                regutils.apply_warp(self.t1w_brain, uatlas, aligned_atlas_skull,
                                    warp=self.mni2t1w_warp, interp='nn', sup=True)

                if uatlas_parcels is not None:
                    aligned_atlas_t1mni_parcels = "%s%s%s%s" % (self.anat_path, '/', atlas, "_t1w_mni_parcels.nii.gz")
                    aligned_atlas_skull_parcels = "%s%s%s%s" % (self.anat_path, '/', atlas, "_t1w_skull_parcels.nii.gz")
                    regutils.applyxfm(self.t1_aligned_mni, uatlas_parcels, self.atlas2t1mni_xfm_init,
                                      aligned_atlas_t1mni_parcels, interp="nearestneighbour")
                    regutils.apply_warp(self.t1w_brain, aligned_atlas_t1mni_parcels, aligned_atlas_skull_parcels,
                                        warp=self.mni2t1w_warp, interp='nn', sup=True)
                    aligned_atlas_t1mni = aligned_atlas_skull_parcels
                else:
                    aligned_atlas_skull_parcels = None

                # Map atlas in t1w space to dwi space
                if uatlas_parcels is not None:
                    regutils.applyxfm(self.ap_path, aligned_atlas_skull_parcels, self.t1wtissue2dwi_xfm,
                                      dwi_aligned_atlas, interp="nearestneighbour")
                else:
                    regutils.applyxfm(self.ap_path, aligned_atlas_skull, self.t1wtissue2dwi_xfm,
                                      dwi_aligned_atlas, interp="nearestneighbour")
            except:
                print("Warning: Atlas is not in correct dimensions, or input is low quality,\nusing linear template "
                      "registration.")

                # Combine our linear transform from t1w to template with our transform from dwi to t1w space to get a
                # transform from atlas ->(-> t1w ->)-> dwi
                regutils.combine_xfms(self.xfm_atlas2t1w_init, self.t1wtissue2dwi_xfm, self.temp2dwi_xfm)

                if uatlas_parcels is not None:
                    aligned_atlas_t1mni_parcels = "%s%s%s%s" % (self.anat_path, '/', atlas, "_t1w_mni_parcels.nii.gz")
                    regutils.applyxfm(self.t1_aligned_mni, uatlas_parcels, self.atlas2t1mni_xfm_init,
                                      aligned_atlas_t1mni_parcels, interp="nearestneighbour")
                    # Apply linear transformation from template to dwi space
                    regutils.applyxfm(self.ap_path, aligned_atlas_t1mni_parcels, self.temp2dwi_xfm, dwi_aligned_atlas,
                                      interp="nearestneighbour")
                    aligned_atlas_t1mni = aligned_atlas_t1mni_parcels
                else:
                    regutils.applyxfm(self.t1_aligned_mni, uatlas, self.atlas2t1mni_xfm_init,
                                      aligned_atlas_t1mni, interp="nearestneighbour")
                    # Apply linear transformation from template to dwi space
                    regutils.applyxfm(self.ap_path, aligned_atlas_t1mni, self.temp2dwi_xfm, dwi_aligned_atlas,
                                      interp="nearestneighbour")
        else:
            # Combine our linear transform from t1w to template with our transform from dwi to t1w space to get a
            # transform from atlas ->(-> t1w ->)-> dwi
            regutils.combine_xfms(self.xfm_atlas2t1w_init, self.t1wtissue2dwi_xfm, self.temp2dwi_xfm)

            if uatlas_parcels is not None:
                aligned_atlas_t1mni_parcels = "%s%s%s%s" % (self.anat_path, '/', atlas, "_t1w_mni_parcels.nii.gz")
                regutils.applyxfm(self.t1_aligned_mni, uatlas_parcels, self.atlas2t1mni_xfm_init,
                                  aligned_atlas_t1mni_parcels, interp="nearestneighbour")
                # Apply linear transformation from template to dwi space
                regutils.applyxfm(self.ap_path, aligned_atlas_t1mni_parcels, self.temp2dwi_xfm, dwi_aligned_atlas,
                                  interp="nearestneighbour")
                aligned_atlas_t1mni = aligned_atlas_t1mni_parcels
            else:
                regutils.applyxfm(self.t1_aligned_mni, uatlas, self.atlas2t1mni_xfm_init,
                                  aligned_atlas_t1mni, interp="nearestneighbour")
                # Apply linear transformation from template to dwi space
                regutils.applyxfm(self.ap_path, aligned_atlas_t1mni, self.temp2dwi_xfm, dwi_aligned_atlas,
                                  interp="nearestneighbour")

        # Set intensities to int
        atlas_img = nib.load(dwi_aligned_atlas)
        t_img = nib.load(self.wm_gm_int_in_dwi)
        mask = math_img('img > 0', img=t_img)
        mask.to_filename(self.wm_gm_int_in_dwi_bin)
        img = nib.Nifti1Image(np.around(np.asarray(atlas_img.dataobj)).astype('uint16'),
                              affine=atlas_img.affine, header=atlas_img.header)
        nib.save(img, dwi_aligned_atlas)
        os.system("fslmaths {} -add {} -bin {} 2>/dev/null".format(dwi_aligned_atlas, self.wm_gm_int_in_dwi_bin,
                                                                   dwi_aligned_atlas_wmgm_int))
        atlas_img.uncache()
        img.uncache()
        mask.uncache()

        return dwi_aligned_atlas_wmgm_int, dwi_aligned_atlas, aligned_atlas_t1mni

    def tissue2dwi_align(self):
        """
        A function to perform alignment of ventricle ROI's from MNI space --> dwi and CSF from T1w space --> dwi.
        First generates and performs dwi space alignment of avoidance/waypoint masks for tractography.
        First creates ventricle ROI. Then creates transforms from stock MNI template to dwi space.
        For this to succeed, must first have called both t1w2dwi_align and atlas2t1w2dwi_align.
        """
        import os.path as op

        # Register Lateral Ventricles and Corpus Callosum rois to t1w
        if not op.isfile(self.mni_atlas):
            raise ValueError('FSL atlas for ventricle reference not found!')

        # Create transform to MNI atlas to T1w using flirt. This will be use to transform the ventricles to dwi space.
        regutils.align(self.mni_atlas, self.input_mni_brain, xfm=self.xfm_roi2mni_init, init=None, bins=None, dof=6,
                       cost='mutualinfo', searchrad=True, interp="spline", out=None)

        # Create transform to align roi to mni and T1w using flirt
        regutils.applyxfm(self.input_mni_brain, self.mni_vent_loc, self.xfm_roi2mni_init, self.vent_mask_mni)

        if self.simple is False:
            # Apply warp resulting from the inverse MNI->T1w created earlier
            regutils.apply_warp(self.t1w_brain, self.vent_mask_mni, self.vent_mask_t1w, warp=self.mni2t1w_warp,
                                interp='nn', sup=True)

            regutils.apply_warp(self.t1w_brain, self.corpuscallosum, self.corpuscallosum_mask_t1w,
                                warp=self.mni2t1w_warp, interp="nn", sup=True)

        else:
            regutils.applyxfm(self.vent_mask_mni, self.t1w_brain, self.mni2t1_xfm, self.vent_mask_t1w)
            regutils.applyxfm(self.corpuscallosum, self.t1w_brain, self.mni2t1_xfm, self.corpuscallosum_mask_t1w)

        # Applyxfm tissue maps to dwi space
        regutils.applyxfm(self.ap_path, self.vent_mask_t1w, self.t1wtissue2dwi_xfm, self.vent_mask_dwi)
        regutils.applyxfm(self.ap_path, self.csf_mask, self.t1wtissue2dwi_xfm, self.csf_mask_dwi)
        regutils.applyxfm(self.ap_path, self.gm_mask, self.t1wtissue2dwi_xfm, self.gm_in_dwi)
        regutils.applyxfm(self.ap_path, self.wm_mask, self.t1wtissue2dwi_xfm, self.wm_in_dwi)
        regutils.applyxfm(self.ap_path, self.corpuscallosum_mask_t1w, self.t1wtissue2dwi_xfm, self.corpuscallosum_dwi)

        # Threshold WM to binary in dwi space
        thr_img = nib.load(self.wm_in_dwi)
        thr_img = math_img('img > 0.20', img=thr_img)
        nib.save(thr_img, self.wm_in_dwi_bin)

        # Threshold GM to binary in dwi space
        thr_img = nib.load(self.gm_in_dwi)
        thr_img = math_img('img > 0.15', img=thr_img)
        nib.save(thr_img, self.gm_in_dwi_bin)

        # Threshold CSF to binary in dwi space
        thr_img = nib.load(self.csf_mask_dwi)
        thr_img = math_img('img > 0.95', img=thr_img)
        nib.save(thr_img, self.csf_mask_dwi_bin)

        # Threshold WM to binary in dwi space
        os.system("fslmaths {} -mas {} {} 2>/dev/null".format(self.wm_in_dwi, self.wm_in_dwi_bin,
                                                              self.wm_in_dwi))

        # Threshold GM to binary in dwi space
        os.system("fslmaths {} -mas {} {} 2>/dev/null".format(self.gm_in_dwi, self.gm_in_dwi_bin,
                                                              self.gm_in_dwi))

        # Threshold CSF to binary in dwi space
        os.system("fslmaths {} -mas {} {} 2>/dev/null".format(self.csf_mask_dwi, self.csf_mask_dwi_bin,
                                                              self.csf_mask_dwi))

        # Create ventricular CSF mask
        print('Creating ventricular CSF mask...')
        os.system("fslmaths {} -kernel sphere 10 -ero -bin {} 2>/dev/null".format(self.vent_mask_dwi,
                                                                                  self.vent_mask_dwi))
        os.system("fslmaths {} -add {} -bin {} 2>/dev/null".format(self.csf_mask_dwi, self.vent_mask_dwi,
                                                                   self.vent_csf_in_dwi))

        print("Creating Corpus Callosum mask...")
        os.system("fslmaths {} -mas {} -sub {} -bin {} 2>/dev/null".format(self.corpuscallosum_dwi,
                                                                           self.wm_in_dwi_bin,
                                                                           self.vent_csf_in_dwi,
                                                                           self.corpuscallosum_dwi))

        # Create gm-wm interface image
        os.system("fslmaths {} -mul {} -add {} -mas {} -bin {} 2>/dev/null".format(self.gm_in_dwi_bin,
                                                                                   self.wm_in_dwi_bin,
                                                                                   self.corpuscallosum_dwi,
                                                                                   self.B0_mask,
                                                                                   self.wm_gm_int_in_dwi))

        return

    def waymask2dwi_align(self, waymask):
        """
        A function to perform alignment of a waymask from MNI space --> T1w --> dwi.
        """

        # Apply warp or transformer resulting from the inverse MNI->T1w created earlier
        if self.simple is False:
            regutils.apply_warp(self.t1w_brain, waymask, self.waymask_in_t1w, warp=self.mni2t1w_warp)
        else:
            regutils.applyxfm(self.t1w_brain, waymask, self.mni2t1_xfm, self.waymask_in_t1w)

        # Apply transform from t1w to native dwi space
        regutils.applyxfm(self.ap_path, self.waymask_in_t1w, self.t1wtissue2dwi_xfm, self.waymask_in_dwi)

        return


class FmriReg(object):
    """
    A Class for Registering an atlas to a subject's MNI-aligned T1w image.
    """

    def __init__(self, basedir_path, anat_file, mask, vox_size, simple):
        import os.path as op
        import pkg_resources
        self.t1w = anat_file
        self.mask = mask
        self.vox_size = vox_size
        self.t1w_name = 't1w'
        self.simple = simple
        self.basedir_path = basedir_path
        self.tmp_path = "%s%s" % (basedir_path, '/fmri_tmp')
        self.reg_path = "%s%s" % (basedir_path, '/fmri_tmp/reg')
        self.anat_path = "%s%s" % (basedir_path, '/anat_reg')
        self.reg_path_mat = "%s%s" % (self.reg_path, '/mats')
        self.reg_path_warp = "%s%s" % (self.reg_path, '/warps')
        self.reg_path_img = "%s%s" % (self.reg_path, '/imgs')
        self.t12mni_xfm_init = "%s%s" % (self.reg_path_mat, "/xfm_t1w2mni_init.mat")
        self.mni2t1_xfm_init = "%s%s" % (self.reg_path_mat, "/xfm_mni2t1w_init.mat")
        self.atlas2t1wmni_xfm_init = "%s%s" % (self.reg_path_mat, "/atlas2t1wmni_xfm_init.mat")
        self.t12mni_xfm = "%s%s" % (self.reg_path_mat, "/xfm_t1w2mni.mat")
        self.mni2t1_xfm = "%s%s" % (self.reg_path_mat, "/xfm_mni2t1.mat")
        self.mni2t1w_warp = "%s%s" % (self.reg_path_warp, "/mni2t1w_warp.nii.gz")
        self.warp_atlas2t1wmni = "%s%s" % (self.reg_path_warp, "/warp_atlas2t1wmni.nii.gz")
        self.warp_t1w2mni = "%s%s" % (self.reg_path_warp, "/t1w2mni_warp.nii.gz")
        self.t1_aligned_mni = "%s%s%s%s" % (self.anat_path, '/', self.t1w_name, "_aligned_mni.nii.gz")
        self.t1w_brain = "%s%s%s%s" % (self.anat_path, '/', self.t1w_name, "_brain.nii.gz")
        self.t1w_brain_mask = "%s%s%s%s" % (self.anat_path, '/', self.t1w_name, "_brain_mask.nii.gz")
        self.map_path = "%s%s%s%s" % (self.anat_path, '/', self.t1w_name, "_seg")
        self.gm_mask = "%s%s%s%s" % (self.anat_path, '/', self.t1w_name, "_gm.nii.gz")
        self.gm_mask_thr = "%s%s%s%s" % (self.anat_path, '/', self.t1w_name, "_gm_thr.nii.gz")
        self.input_mni = pkg_resources.resource_filename("pynets", "templates/MNI152_T1_" + vox_size + ".nii.gz")
        self.input_mni_brain = pkg_resources.resource_filename("pynets", "templates/MNI152_T1_" + vox_size +
                                                               "_brain.nii.gz")
        self.input_mni_mask = pkg_resources.resource_filename("pynets", "templates/MNI152_T1_" + vox_size +
                                                              "_brain_mask.nii.gz")

        # Create empty tmp directories that do not yet exist
        reg_dirs = [self.tmp_path, self.reg_path, self.anat_path, self.reg_path_mat, self.reg_path_warp,
                    self.reg_path_img]
        for i in range(len(reg_dirs)):
            if not op.isdir(reg_dirs[i]):
                os.mkdir(reg_dirs[i])

        if op.isfile(self.t1w_brain) is False:
            import shutil
            shutil.copyfile(self.t1w, self.t1w_brain)

    def gen_tissue(self, overwrite=False):
        """
        A function to segment and threshold tissue types from T1w.
        """
        import glob
        import os.path as op

        # Apply brain mask if detected as a separate file
        try:
            anat_mask_existing = glob.glob(op.dirname(self.t1w) + '/*_desc-brain_mask.nii.gz')[0]
            if op.isfile(anat_mask_existing) and not self.mask and overwrite is False:
                anat_mask_existing = regutils.check_orient_and_dims(anat_mask_existing, self.basedir_path,
                                                                    self.vox_size)
                try:
                    os.system("fslmaths {} -mas {} {} 2>/dev/null".format(self.t1w_brain, anat_mask_existing,
                                                                          self.t1w_brain))
                except:
                    try:
                        from nilearn.image import resample_to_img
                        nib.save(resample_to_img(nib.load(anat_mask_existing), nib.load(self.t1w_brain)),
                                 anat_mask_existing)
                        os.system("fslmaths {} -mas {} {} 2>/dev/null".format(self.t1w_brain, anat_mask_existing,
                                                                              self.t1w_brain))
                    except ValueError:
                        print('Cannot coerce mask to shape of T1w anatomical.')

            # Segment the t1w brain into probability maps
            gm_mask_existing = glob.glob(op.dirname(self.t1w) + '/*_label-GM_probseg.nii.gz')[0]
        except:
            anat_mask_existing = None
            gm_mask_existing = None

        if gm_mask_existing:
            if op.isfile(gm_mask_existing) and overwrite is False:
                out_gm_mask = regutils.check_orient_and_dims(gm_mask_existing, self.basedir_path, self.vox_size,
                                                             overwrite=False)
            else:
                try:
                    maps = regutils.segment_t1w(self.t1w_brain, self.map_path)
                except RuntimeError:
                    print('Segmentation failed. Does the input anatomical image still contained skull?')
                out_gm_mask = maps['gm_prob']
        else:
            try:
                maps = regutils.segment_t1w(self.t1w_brain, self.map_path)
            except RuntimeError:
                print('Segmentation failed. Does the input anatomical image still contained skull?')
            out_gm_mask = maps['gm_prob']

        # Threshold GM to binary in func space
        t_img = nib.load(out_gm_mask)
        mask = math_img('img > 0.05', img=t_img)
        mask.to_filename(self.gm_mask_thr)
        os.system("fslmaths {} -mas {} {} 2>/dev/null".format(out_gm_mask, self.gm_mask_thr, self.gm_mask))

        # Threshold T1w brain to binary in anat space
        t_img = nib.load(self.t1w_brain)
        mask = math_img('img > 0.0', img=t_img)
        mask.to_filename(self.t1w_brain_mask)

        return

    def t1w2mni_align(self):
        """
        A function to perform alignment from T1w --> MNI.
        """
        # Create linear transform/ initializer T1w-->MNI
        regutils.align(self.t1w_brain, self.input_mni_brain, xfm=self.t12mni_xfm_init, bins=None, interp="spline",
                       out=None, dof=12, cost='mutualinfo', searchrad=True)

        # Attempt non-linear registration of T1 to MNI template
        try:
            print('Running non-linear registration: T1w-->MNI ...')
            # Use FNIRT to nonlinearly align T1 to MNI template
            regutils.align_nonlinear(self.t1w_brain, self.input_mni, xfm=self.t12mni_xfm_init, out=self.t1_aligned_mni,
                                     warp=self.warp_t1w2mni, ref_mask=self.input_mni_mask)

        except RuntimeError('Error: FNIRT failed!'):
            pass

    def atlas2t1wmni_align(self, uatlas, uatlas_parcels, atlas):
        """
        A function to perform atlas alignment from atlas --> T1_MNI.
        """
        from nilearn.image import resample_img

        aligned_atlas_t1mni = "%s%s%s%s" % (self.anat_path, '/', atlas, "_t1w_mni.nii.gz")
        gm_mask_mni = "%s%s%s%s" % (self.anat_path, '/', atlas, "_gm_mask_t1w_mni.nii.gz")
        gm_mask_mni_atlas_res = "%s%s%s%s" % (self.anat_path, '/', atlas, "_gm_mask_t1w_mni_res.nii.gz")
        aligned_atlas_t1mni_gm = "%s%s%s%s" % (self.anat_path, '/', atlas, "_t1w_mni_gm.nii.gz")

        uatlas_filled = "%s%s%s%s" % (self.anat_path, '/', atlas, "_filled.nii.gz")
        os.system("fslmaths {} -add {} -mas {} {} 2>/dev/null".format(self.input_mni_brain, uatlas,
                                                                      self.input_mni_mask, uatlas_filled))

        regutils.align(uatlas_filled, self.t1_aligned_mni, init=None, xfm=self.atlas2t1wmni_xfm_init,
                       out=None, dof=12, searchrad=True, interp="nearestneighbour", cost='mutualinfo')

        if uatlas_parcels is not None:
            regutils.applyxfm(self.t1_aligned_mni, uatlas_parcels, self.atlas2t1wmni_xfm_init, aligned_atlas_t1mni,
                              interp="nearestneighbour")
        else:
            regutils.applyxfm(self.t1_aligned_mni, uatlas, self.atlas2t1wmni_xfm_init, aligned_atlas_t1mni,
                              interp="nearestneighbour")

        try:
            regutils.apply_warp(self.t1_aligned_mni, self.gm_mask, gm_mask_mni, warp=self.warp_t1w2mni,
                                xfm=self.t12mni_xfm_init, interp='nn', sup=True)
        except:
            regutils.applyxfm(self.t1_aligned_mni, self.gm_mask, self.t12mni_xfm_init, gm_mask_mni,
                              interp="nearestneighbour")

        # Set intensities to int
        atlas_img = nib.load(aligned_atlas_t1mni)
        gm_mask_img_res = resample_img(nib.load(gm_mask_mni), target_affine=atlas_img.affine,
                                       target_shape=atlas_img.shape)
        nib.save(gm_mask_img_res, gm_mask_mni_atlas_res)
        os.system("fslmaths {} -bin {} 2>/dev/null".format(gm_mask_mni_atlas_res, gm_mask_mni_atlas_res))
        os.system("fslmaths {} -mas {} {} 2>/dev/null".format(aligned_atlas_t1mni, gm_mask_mni_atlas_res,
                                                              aligned_atlas_t1mni_gm))

        gm_mask_img_res.uncache()
        atlas_img.uncache()

        return aligned_atlas_t1mni_gm


def register_atlas_dwi(uatlas, uatlas_parcels, atlas, node_size, basedir_path, fa_path, ap_path, B0_mask, anat_file,
                       coords, labels, gm_in_dwi, vent_csf_in_dwi, wm_in_dwi, gtab_file, dwi_file, mask,
                       vox_size, simple=False):
    """
    A Function to register an atlas to T1w-warped MNI-space, and restrict the atlas to grey-matter only.

    Parameters
    ----------
    uatlas : str
        File path to atlas parcellation Nifti1Image in MNI template space.
    uatlas_parcels : str
        File path to subset atlas parcellation Nifti1Image in MNI template space, if any.
    atlas : str
        Name of atlas parcellation used.
    node_size : int
        Spherical centroid node size in the case that coordinate-based centroids
        are used as ROI's for tracking.
    basedir_path : str
        Path to directory to output direct-streamline normalized temp files and outputs.
    fa_path : str
        File path to FA Nifti1Image.
    ap_path : str
        File path to anisotropic power Nifti1Image.
    B0_mask : str
        File path to B0 brain mask.
    anat_file : str
        Path to a skull-stripped anatomical Nifti1Image.
    coords : list
        List of (x, y, z) tuples corresponding to the center-of-mass of each parcellation node.
    labels : list
        List of string labels corresponding to graph nodes.
    gm_in_dwi : str
        File path to grey-matter tissue segmentation Nifti1Image in native diffusion space.
    vent_csf_in_dwi : str
        File path to ventricular CSF tissue segmentation Nifti1Image in native diffusion space.
    wm_in_dwi : str
        File path to white-matter tissue segmentation Nifti1Image in native diffusion space.
    gtab_file : str
        File path to pickled DiPy gradient table object.
    dwi_file : str
        File path to diffusion weighted image.
    mask : str
        Path to a brain mask to apply to the anatomical Nifti1Image.
    vox_size : str
        Voxel size in mm. (e.g. 2mm).
    simple : bool
        Indicates whether to use non-linear registration and BBR (True) or entirely linear methods (False).
        Default is False.

    Returns
    -------
    dwi_aligned_atlas_t1mni_wmgm_int : str
        File path to atlas parcellation Nifti1Image in T1w-MNI warped native diffusion space, restricted only to wm-gm
        interface.
    dwi_aligned_atlas : str
        File path to atlas parcellation Nifti1Image in native diffusion space.
    aligned_atlas_t1mni : str
        File path to atlas parcellation Nifti1Image in T1w-warped MNI space.
    uatlas : str
        File path to atlas parcellation Nifti1Image in MNI template space.
    atlas : str
        Name of atlas parcellation used.
    coords : list
        List of (x, y, z) tuples corresponding to the center-of-mass of each parcellation node.
    labels : list
        List of string labels corresponding to graph nodes.
    node_size : int
        Spherical centroid node size in the case that coordinate-based centroids
        are used as ROI's for tracking.
    gm_in_dwi : str
        File path to grey-matter tissue segmentation Nifti1Image in native diffusion space.
    vent_csf_in_dwi : str
        File path to ventricular CSF tissue segmentation Nifti1Image in native diffusion space.
    wm_in_dwi : str
        File path to white-matter tissue segmentation Nifti1Image in native diffusion space.
    fa_path : str
        File path to FA Nifti1Image.
    gtab_file : str
        File path to pickled DiPy gradient table object.
    B0_mask : str
        File path to B0 brain mask.
    dwi_file : str
        File path to diffusion weighted image.
    """
    from pynets.registration import register

    reg = register.DmriReg(basedir_path, fa_path, ap_path, B0_mask, anat_file, mask, vox_size, simple)

    if node_size is not None:
        atlas = "%s%s%s" % (atlas, '_', node_size)

    # Apply warps/coregister atlas to dwi
    if uatlas == uatlas_parcels:
        uatlas_parcels = None
    [dwi_aligned_atlas_wmgm_int, dwi_aligned_atlas, aligned_atlas_t1mni] = reg.atlas2t1w2dwi_align(uatlas,
                                                                                                   uatlas_parcels,
                                                                                                   atlas)

    return (dwi_aligned_atlas_wmgm_int, dwi_aligned_atlas, aligned_atlas_t1mni, uatlas, atlas, coords, labels,
            node_size, gm_in_dwi, vent_csf_in_dwi, wm_in_dwi, ap_path, gtab_file, B0_mask, dwi_file)


def register_atlas_fmri(uatlas, uatlas_parcels, atlas, basedir_path, anat_file, vox_size, mask, reg_fmri_complete,
                        simple=False):
    """
    A Function to register an atlas to T1w-warped MNI-space, and restrict the atlas to grey-matter only.

    Parameters
    ----------
    uatlas : str
        File path to atlas parcellation Nifti1Image in MNI template space.
    uatlas_parcels : str
        File path to subset atlas parcellation Nifti1Image in MNI template space, if any.
    atlas : str
        Name of atlas parcellation used.
    basedir_path : str
        Path to directory to output direct-streamline normalized temp files and outputs.
    anat_file : str
        Path to a skull-stripped anatomical Nifti1Image.
    vox_size : str
        Voxel size in mm. (e.g. 2mm).
    mask : str
        Path to a brain mask to apply to the anatomical Nifti1Image.
    reg_fmri_complete : bool
        Indicates whether initial registration is complete.
    simple : bool
        Indicates whether to use non-linear registration (True) or entirely linear methods (False).
        Default is False.

    Returns
    -------
    aligned_atlas_t1mni_gm : str
        File path to atlas parcellation Nifti1Image in T1w-warped MNI space, restricted only to grey-matter.
    """
    from pynets.registration import register

    reg = register.FmriReg(basedir_path, anat_file, mask, vox_size, simple)

    # Apply warps/coregister atlas to t1w_mni
    if uatlas == uatlas_parcels:
        uatlas_parcels = None

    aligned_atlas_t1mni_gm = reg.atlas2t1wmni_align(uatlas, uatlas_parcels, atlas)

    return aligned_atlas_t1mni_gm
