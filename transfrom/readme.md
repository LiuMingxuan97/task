# &#x20;几何校正算法 &#x20;

## &#x20;文件说明&#x20;

*   demo\_01.py          初版几何定位  &#x20;

<!---->

*   demo\_02.py          改进版  &#x20;

<!---->

*   demo\_03.py          完整版，需输入ecef下的坐标、速度和时间  &#x20;

<!---->

*   eci\_rpy\_finsh.py    eci完整版  &#x20;

<!---->

*   earth\_latest\_high\_prec.bpc  &#x20;

<!---->

*   naif0012.tls        spice需要的两个文件 &#x20;

    ## 算法说明

    1.  建立像元的真实坐标

        ```python
        def pos_cam(pix_cam_id, Px):
            pos_cam_mm = np.array([pix_cam_id[0] *Px , pix_cam_id[1]*Px, 1])
            return pos_cam_mm
        ```
    2.  建立相机坐标

        ```python
        def img2cam(Px, Py, F, principal_point_x, principal_point_y):
            fc = F
            x0 = principal_point_x * Px
            y0 = principal_point_y * Py
            R_img2cam = np.array([[1, 0, -x0],
                                  [0, 1, -y0],
                                  [0, 0, -fc]])
            return R_img2cam
        ```
    3.  建立卫星坐标

        ```python
        def cam2body():
            R_cam2body = np.array([[1, 0, 0],
                                   [0, 1, 0],
                                   [0, 0, 1]])
            return R_cam2body
        ```
    4.  建立轨道坐标

        ```python
        def body2orb(roll, pitch, yaw):
            R_x = np.array([[1, 0, 0],
                        [0, cos(roll), sin(roll)],
                        [0, -sin(roll), cos(roll)]])
            R_y = np.array([[cos(pitch), 0, -sin(pitch)],
                        [0, 1, 0],
                        [sin(pitch), 0, cos(pitch)]])
            R_z = np.array([[cos(yaw), sin(yaw), 0],
                        [-sin(yaw), cos(yaw), 0],
                        [0, 0,1 ]])
            R_body2orb= np.dot(R_x,np.dot(R_y,R_z)).T
            return R_body2orb
        ```
    5.  ecef坐标系下位置、速度转eci下位置、速度

        ```python
        def ecr2eci(obs_pos, obs_vel, satatime):
            sate_time = arrow.get(satatime)
            sate_time = sate_time.datetime
            date_str = sate_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            spice.furnsh('/Users/liumingxuan/code/pycode/transfrom/naif0012.tls')
            spice.furnsh('/Users/liumingxuan/code/pycode/transfrom/earth_latest_high_prec.bpc')
            et = spice.str2et(date_str)
            mat = spice.pxform('ITRF93', 'J2000', et)
            mat66_r2i = spice.sxform('ITRF93', 'J2000', et)
            epos, estate = [0] * 3, [0] * 6
            for i in range(3):
                epos[i] = obs_pos[i]
                estate[i] = obs_pos[i]
                estate[i+3] = obs_vel[i]
                jpos = spice.mxv(mat, epos)
                jstate = spice.mxvg(mat66_r2i, estate)
                eci_pos, eci_vel = [0] *3, [0] *3
            for i in range(3):
                eci_pos[i] = jpos[i]
                eci_vel[i] = jstate[i+3]
            return eci_pos, eci_vel
        ```
    6.  建立eci坐标

        ```python
        def orb2eci(r_ECI, v_ECI):
            '''
            :r_ECI   地固系通过spice转换为地惯系位置
            :v_ECI   地固系通过spice转换为地惯系速度
            '''
            R_orb2eci = np.ndarray(shape=(3,3), dtype=float, order='F')
            b3 = np.zeros(3)
            b2 = np.zeros(3)
            b1 = np.zeros(3)
            temp = np.zeros(3)

            for i in range(3):
                b3[i] = -1 * r_ECI[i] / np.linalg.norm(r_ECI)
            temp = np.cross(b3, v_ECI)
            norm = np.linalg.norm(temp)

            for i in range(3):
                b2[i] = temp[i] / norm
                
            b1 = np.cross(b2 , b3)
            R_orb2eci = np.vstack((b1, b2, b3)).T
            return R_orb2eci
        ```
    7.  四元数转换为旋转矩阵

        ```python
        def q_rotation(q_list:list):
            # 创建旋转矩阵对象
            r = Rotation.from_quat(q_list)
            R_body2eci_q = r.as_matrix()
            return R_body2eci_q
        ```
    8.  建立ecec坐标

        ```python
        def eci2ecr(satatime):
            R_eci2ecr = np.ndarray(shape=(3,3), dtype=float, order='F')
            sate_time = arrow.get(satatime)
            sate_time = sate_time.datetime
            date_str = sate_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            spice.furnsh('/Users/liumingxuan/code/pycode/transfrom/naif0012.tls')
            spice.furnsh('/Users/liumingxuan/code/pycode/transfrom/earth_latest_high_prec.bpc')
            et = spice.str2et(date_str)
            mat = spice.pxform('J2000', 'ITRF93',  et)
            for i in range(3):
                for j in range(3):
                    R_eci2ecr[i,j] = mat[i][j] / pow(3,0.5)
            return R_eci2ecr
        ```

