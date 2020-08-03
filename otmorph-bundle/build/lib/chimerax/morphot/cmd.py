from chimerax.core.commands import CmdDesc, register, BoolArg, StringArg, EnumOf, IntArg, Int3Arg, ModelIdArg
from chimerax.map import MapsArg, MapStepArg, Float1or3Arg, ValueTypeArg
from chimerax.map.mapargs import Float2Arg, MapRegionArg
from chimerax.core.errors import UserError as CommandError
import numpy as np

def volume_morphOT(session, volumes, frames = 25, start = 0, play_step = 0.04,
            play_direction = 1, niter = 20, reg = None, rate = 'linear',  play_range = None, add_mode = False,
            constant_volume = False, scale_factors = None,
            hide_original_maps = True, interpolate_colors = True, maxsize = 60,
            subregion = 'all', step = 1, model_id = None):
    '''OT interpolate between maps.'''
    
    if len(volumes) < 2:
        raise CommandError('volume morph requires 2 or more volumes, got %d' % len(volumes))
    if play_range is None:
        if add_mode:
            prange = (-1.0,1.0)
        else:
            prange = (0.0,1.0)
    else:
        prange = play_range

    if not scale_factors is None and len(volumes) != len(scale_factors):
        raise CommandError('Number of scale factors (%d) does not match number of volumes (%d)'
                            % (len(scale_factors), len(volumes)))
    vs = [tuple(v.matrix_size(step = step, subregion = subregion))
            for v in volumes]

    if len(set(vs)) > 1:
        sizes = ' and '.join([str(s) for s in vs])
        raise CommandError("Volume grid sizes don't match: %s" % sizes)



    if frames > 0 :
        #play_step = 1./frames   #bounces back
        play_step = (prange[-1] - prange[0]) / float(frames)  #doesnt bounce back

    if np.product(vs[0]) > maxsize**3 : 
        print('Your structure is bigger than maxsize, you might consider using barycenterSave for efficiency issue')
        print('resizing volumes to maxsize')
        downscale_ratio = round(max(list(set(vs))[0])/maxsize)
        step = downscale_ratio 

    

    if reg == None : 
        reg = max(volumes[0].matrix(step = step, subregion = subregion).shape) / 60.

<<<<<<< HEAD
    session.logger.info('Coucou')
=======
    print(reg)
>>>>>>> 1b176815f5ce5e21c4a63bad2b944230a863b92a

    from .mergedmorph import morph_maps_ot
    im = morph_maps_ot(volumes, frames, start, play_step, play_direction, prange,
                    add_mode, constant_volume, scale_factors,
                    hide_original_maps, interpolate_colors, subregion, step, model_id, niter, reg, rate)

    return im


def volume_semi_morphOT(session, volumes, frames = 25, ot_frames = 4, start = 0, play_step = 0.04,
            play_direction = 1, niter = 20, reg = None, rate = 'linear',  play_range = None, add_mode = False,
            constant_volume = False, scale_factors = None,
            hide_original_maps = True, interpolate_colors = True, maxsize = 60,
            subregion = 'all', step = 1, model_id = None, precompute = False):
    '''OT interpolate between maps.'''
    
    if len(volumes) < 2:
        raise CommandError('volume morph requires 2 or more volumes, got %d' % len(volumes))
    if play_range is None:
        if add_mode:
            prange = (-1.0,1.0)
        else:
            prange = (0.0,1.0)
    else:
        prange = play_range

    if not scale_factors is None and len(volumes) != len(scale_factors):
        raise CommandError('Number of scale factors (%d) does not match number of volumes (%d)'
                            % (len(scale_factors), len(volumes)))
    vs = [tuple(v.matrix_size(step = step, subregion = subregion))
            for v in volumes]

    if len(set(vs)) > 1:
        sizes = ' and '.join([str(s) for s in vs])
        raise CommandError("Volume grid sizes don't match: %s" % sizes)



    if frames > 0 :
        play_step = 1./frames


    if np.product(vs[0]) > maxsize**3 : 
        print('Your structure is bigger than maxsize, you might consider using barycenterSave for efficiency issue')
        print('resizing volumes to maxsize')
        downscale_ratio = round(max(list(set(vs))[0])/maxsize)
        step = downscale_ratio 

    print(step)

    if reg == None : 
        reg = max(volumes[0].matrix(step = step, subregion = subregion).shape) / 60.

    
    from .mergedmorph import semi_morph_maps_ot
    im = semi_morph_maps_ot(volumes, frames, ot_frames, start, play_step, play_direction, prange,
                    add_mode, constant_volume, scale_factors,
                    hide_original_maps, interpolate_colors, subregion, step, model_id, niter, reg, rate, precompute)

    return im


def volume_barycenterOT(session, volumes, weights, niter = 20, reg = None, interpolate_colors = True,
            subregion = 'all', step = 1, model_id = None, maxsize = 60):
    '''OT interpolate between maps.'''
    if len(volumes) < 2:
        raise CommandError('volume morph requires 2 or more volumes, got %d' % len(volumes))

    vs = [tuple(v.matrix_size(step = step, subregion = subregion))
            for v in volumes]


    if len(set(vs)) > 1:
        sizes = ' and '.join([str(s) for s in vs])
        raise CommandError("Volume grid sizes don't match: %s" % sizes)

    if reg == None : 
        reg = max(volumes[0].matrix(step = step, subregion = subregion).shape)/60.

    


    """if np.product(vs[0]) > maxsize**3 : 
        print('Your structure is bigger than maxsize, you might consider using barycenterSave for efficiency issue')
        print('resizing volumes to maxsize')
        downscale_ratio = round(max(list(set(vs))[0])/maxsize)
        step = downscale_ratio """


    from .mergedmorph import ot_barycenter

    im = ot_barycenter(volumes, weights, niter, reg, subregion, step, model_id) 

    return im



def volume_barycenterSave(session, volumes, folder, frames = 25, niter = 20, reg = None, rate = 'Linear', interpolate_colors = True,
            subregion = 'all', step = 1, model_id = None, maxsize = 60, name1 = None, name2 = None):
    '''OT interpolate between maps.'''
    if len(volumes) < 2:
        raise CommandError('volume morph requires 2 or more volumes, got %d' % len(volumes))


    vs = [tuple(v.matrix_size(step = step, subregion = subregion))
            for v in volumes]
    if len(set(vs)) > 1:
        sizes = ' and '.join([str(s) for s in vs])
        raise CommandError("Volume grid sizes don't match: %s" % sizes)
    
    import pathlib

    if frames > 0 :
        play_step = 1./frames


    if np.product(vs[0]) > maxsize**3 : 
        print('Your structure is bigger than maxsize, you might consider using barycenterSave for efficiency issue')
        print('resizing volumes to maxsize')
        downscale_ratio = round(max(list(set(vs))[0])/maxsize)
        step = downscale_ratio 

    if reg == None : 
        reg = max(volumes[0].matrix(step = step, subregion = subregion).shape)/60.

    from .mergedmorph import ot_save

    ot_save(volumes, folder, frames, niter, reg, rate, subregion, step, model_id, name1, name2)


def volume_linearBarycenterSave(session, volumes, folder, frames = 25, niter = 20, reg = None, rate = 'Linear', interpolate_colors = True,
            subregion = 'all', step = 1, model_id = None, maxsize = 60):
    '''OT interpolate between maps.'''
    if len(volumes) < 2:
        raise CommandError('volume morph requires 2 or more volumes, got %d' % len(volumes))


    vs = [tuple(v.matrix_size(step = step, subregion = subregion))
            for v in volumes]
    if len(set(vs)) > 1:
        sizes = ' and '.join([str(s) for s in vs])
        raise CommandError("Volume grid sizes don't match: %s" % sizes)
    
    import pathlib

    if frames > 0 :
        play_step = 1./frames


    if np.product(vs[0]) > maxsize**3 : 
        print('Your structure is bigger than maxsize, you might consider using barycenterSave for efficiency issue')
        print('resizing volumes to maxsize')
        downscale_ratio = round(max(list(set(vs))[0])/maxsize)
        step = downscale_ratio

    if reg == None : 
        reg = max(volumes[0].matrix(step = step, subregion = subregion).shape)/60.

    from .mergedmorph import linear_save

    linear_save(volumes, folder, frames, niter, reg, rate, subregion, step, model_id)




varg = [('volumes', MapsArg)]
ssm_kw = [
    ('subregion', MapRegionArg),
    ('step', MapStepArg),
    ('model_id', ModelIdArg),
]