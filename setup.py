# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md', encoding="utf-8") as f:
    readme = f.read()

setup(
    name='meile-gui',
<<<<<<< HEAD
    version='1.1.0',
=======
    version='0.9.9-beta.1',
>>>>>>> 80ab241e269da90baefd4b857339cce30a324ecb
    description='Meile dVPN powered by the Sentinel Network',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='MathNodes',
    author_email='freQniK@mathnodes.com',
    url='https://github.com/MathNodes/meile-gui',
    license='GNU General Public License (GPL)',
    keywords='vpn, dvpn, sentinel, crypto, gui, privacy, security, decentralized ',
    classifiers = [
        'Development Status :: 4 - Beta',
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Environment :: X11 Applications",
        "Environment :: MacOS X",
        "Intended Audience :: Information Technology",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.8",
        "Topic :: System :: Networking",
        "Topic :: Internet",
        
        
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=['kivymd', 'pydash', 'treelib', 'kivyoav', 'pexpect', 'qrcode', 'save_thread_result', 'screeninfo', 'stripe', 'pycoingecko'],
    package_data={'conf': ['config/config.ini'], 'bin' : ['sentinelcli', 'warp-cli', 'warp-svc'], 'awoc' : ['data/world.json'],
                  'fonts': ['Roboto-BoldItalic.ttf'], 'imgs' : ["ad.png","ae.png","af.png","ag.png",
                                                              "ai.png","al.png","am.png","ao.png",
                                                              "aq.png","ar.png","as.png","atom.png",
                                                              "at.png","au.png","avg.png","aw.png",
                                                              "ax.png","az.png","ba.png","bb.png",
                                                              "bd.png","be.png","bf.png","bg.png",
                                                              "bh.png","bi.png","bj.png","bl.png",
                                                              "bm.png","bn.png","bo.png","bq.png",
                                                              "br.png","bs.png","bt.png","bv.png",
                                                              "bw.png","by.png","bz.png","ca.png",
                                                              "cc.png","cd.png","cf.png","cg.png",
                                                              "ch.png","ci.png","ck.png","cl.png",
                                                              "cm.png","cn.png","co.png","cr.png",
                                                              "cu.png","cv.png","cw.png","cx.png",
                                                              "cy.png","cz.png","dec.png","de.png",
                                                              "dj.png","dk.png","dm.png","do.png",
                                                              "dvpn.png","dz.png","ec.png","ee.png",
                                                              "eg.png","eh.png","er.png","es.png",
                                                              "et.png","fastavg.png","fast.png",
                                                              "fi.png","fj.png","fk.png","fm.png",
                                                              "fo.png","fr.png","ga.png","gb-eng.png",
                                                              "gb-nir.png","gb.png","gb-sct.png",
                                                              "gb-wls.png","gd.png","ge.png","gf.png"
                                                              ,"gg.png","gh.png","gi.png","gl.png",
                                                              "gm.png","gn.png","gp.png","gq.png",
                                                              "gr.png","gs.png","gt.png","gu.png",
                                                              "gw.png","gy.png","hk.png","hm.png",
                                                              "hn.png","hr.png","ht.png","hu.png",
                                                              "icon.png","id.png","ie.png","il.png",
                                                              "imgage_list.sh","im.png","in.png","io.png",
                                                              "iq.png","ir.png","is.png","it.png",
                                                              "je.png","jm.png","jo.png","jp.png",
                                                              "ke.png","kg.png","kh.png","ki.png",
                                                              "km.png","kn.png","kp.png","kr.png",
                                                              "kw.png","ky.png","kz.png","la.png",
                                                              "lb.png","lc.png","li.png","lk.png",
                                                              "logo_hd.png","logo.png","lr.png",
                                                              "ls.png","lt.png","lu.png","lv.png",
                                                              "ly.png","ma.png","mc.png","md.png",
                                                              "me.png","mf.png","mg.png","mh.png",
                                                              "mk.png","ml.png","mm.png","mn.png",
                                                              "mo.png","mp.png","mq.png","mr.png",
                                                              "ms.png","mt.png","mu.png","mv.png",
                                                              "mw.png","mx.png","my.png","mz.png",
                                                              "na.png","nc.png","ne.png","nf.png",
                                                              "ng.png","ni.png","nl.png","no.png",
                                                              "np.png","nr.png","nu.png","nz.png",
                                                              "om.png","osmo.png","pa.png","pe.png",
                                                              "pf.png","pg.png","ph.png","pk.png",
                                                              "pl.png","pm.png","pn.png","pr.png",
                                                              "ps.png","pt.png","pw.png","py.png",
                                                              "qa.png","re.png","ro.png","rs.png",
                                                              "ru.png","rw.png","sa.png","sb.png",
                                                              "sc.png","scrt.png","sd.png","se.png",
                                                              "sg.png","sh.png","si.png","sj.png",
                                                              "sk.png","slowavg.png","slow.png","sl.png",
                                                              "sm.png","sn.png","so.png","sr.png","ss.png",
                                                              "st.png","sv.png","sx.png","sy.png","sz.png",
                                                              "tc.png","td.png","tenor.gif","tf.png",
                                                              "tg.png","th.png","tj.png","tk.png","tl.png",
                                                              "tm.png","tn.png","to.png","tr.png","tt.png",
                                                              "tv.png","tw.png","tz.png","ua.png","ug.png",
                                                              "um.png","us.png","uy.png","uz.png","va.png",
                                                              "vc.png","ve.png","vg.png","vi.png","vn.png",
                                                              "vu.png","wf.png","ws.png","xk.png","ye.png",
                                                              "yt.png","za.png","zm.png","zw.png", "protected.png"], 
                  'kv' : ['meile.kv'], 'main' : ['icon.png'], 'utils' :  ['coinimg/dvpn.png', 'fonts/Roboto-BoldItalic.ttf']  },
    entry_points = {
        'console_scripts': ['meile-gui = main.meile_gui:main'],
    }
)
