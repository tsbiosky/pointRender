import numpy as np

def standardize_bbox(pcl, points_per_object):
    #pt_indices = np.random.choice(pcl.shape[0], points_per_object, replace=False)
    #np.random.shuffle(pt_indices)
    #pcl = pcl[pt_indices] # n by 3
    mins = np.amin(pcl, axis=0)
    maxs = np.amax(pcl, axis=0)
    center = ( mins + maxs ) / 2.
    scale = np.amax(maxs-mins)
    print("Center: {}, Scale: {}".format(center, scale))
    result = ((pcl - center)/scale).astype(np.float32) # [-0.5, 0.5]
    return result

xml_head = \
"""
<scene version="2.0.0">
    <integrator type="path">
        <integer name="max_depth" value="-1"/>
    </integrator>
    <sensor type="perspective">
        <float name="far_clip" value="100"/>
        <float name="near_clip" value="0.1"/>
        <transform name="to_world">
            <lookat origin="3,3,3" target="0,0,0" up="0,0,1"/>
        </transform>
        <float name="fov" value="25"/>
        
        <sampler type="independent">
            <integer name="sample_count" value="256"/>
        </sampler>
        <film type="hdrfilm">
            <integer name="width" value="1600"/>
            <integer name="height" value="1200"/>
            <rfilter type="gaussian"/>
            <boolean name="banner" value="false"/>
        </film>
    </sensor>
    
    <bsdf type="roughplastic" id="surfaceMaterial">
        <string name="distribution" value="ggx"/>
        <float name="alpha" value="0.05"/>
        <float name="int_ior" value="1.46"/>
        
    </bsdf>
    
"""

xml_ball_segment = \
"""
    <shape type="sphere">
        <float name="radius" value="0.01"/>
        <transform name="to_world">
            <translate x="{}" y="{}" z="{}"/>
        </transform>
        <bsdf type="diffuse">
            <rgb name="reflectance" value="{},{},{}"/>
        </bsdf>
    </shape>
"""

xml_tail = \
"""
    <shape type="rectangle">
        <ref name="bsdf" id="surfaceMaterial"/>
        <transform name="to_world">
            <scale x="10" y="10" z="1"/>
            <translate x="0" y="0" z="-0.5"/>
        </transform>
    </shape>
    
    <shape type="rectangle">
        <transform name="to_world">
            <scale x="10" y="10" z="1"/>
            <lookat origin="-4,4,20" target="0,0,0" up="0,0,1"/>
        </transform>
        <emitter type="area">
            <rgb name="radiance" value="6,6,6"/>
        </emitter>
    </shape>
</scene>
"""

def colormap(x,y,z):
    vec = np.array([x,y,z])
    vec = np.clip(vec, 0.001,1.0)
    norm = np.sqrt(np.sum(vec**2))
    vec /= norm
    return [vec[0], vec[1], vec[2]]
xml_segments = [xml_head]

#tt= np.load('vis_adv.npz')
tt= np.load('hd.npz')

pcl=tt['hd']
#index=tt['index']
pcl = standardize_bbox(pcl, pcl.shape[0])
pcl = pcl[:,[2,0,1]]
pcl[:,0] *= -1
pcl[:,2] += 0.0125
blue=[65/255.0,105/255.0,225/255.0]
red=[1,0,0]
for i in range(pcl.shape[0]):
    #color = colormap(pcl[i,0]+0.5,pcl[i,1]+0.5,pcl[i,2]+0.5-0.0125)
    '''
    if i in index:
        color=red
    else:
        color=blue
    '''
    color = blue
    xml_segments.append(xml_ball_segment.format(pcl[i,0],pcl[i,1],pcl[i,2], *color))
xml_segments.append(xml_tail)

xml_content = str.join('', xml_segments)

with open('hd_airplane.xml', 'w') as f:
    f.write(xml_content)


