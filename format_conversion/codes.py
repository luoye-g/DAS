
'''
    编码与类别匹配
    0700:       错误类别编码 wrong
    阴性新增类别与对应编码
    'nplus':        0801
    'singel':       0802
    'several':      0803
    'tens':         0804
    'bubble':       0805
    删除的标注
    'deleted_0.0'   0806
    'deleted_0.100' 0807
    阳性
    'pos'           0809
    未知
    'mould'         0810
    'nn'            0811
    'pp'            0812
    'Neg'           0813
    'pos_jp'        0814
    model3:
    'typical_pos'   0900
    'nplus'         0902
    'cornified'     0903
    'superficial'   0904
    'atrophy'       0905
'''
class cc:
    code_to_class = {
        '2112': 'ASC-H',
        '2111': 'ASCUS',
        '2130': 'HSIL',
        '0200': 'nGEC',
        '2120': 'LSIL',
        '3000': 'others',
        '2222': 'AGC',
        '2211': 'AEC',
        '2140': 'SCC',
        '2213': 'AGC_NOS',
        '0000': 'normal_0000',
        '0100': 'normal_0100',
        '0300': 'normal_0300',
        '0400': 'normal_0400',
        '0500': 'normal_0500',
        '0600': 'normal_0600',
        '1111': 'Squamous_metaplastic',  # Squamous metaplastic(鳞状化生)
        '1123': 'IUD',  # 宫内节育器
        '1112': 'Keratosis',  # Keratosis(角化改变)
        '1211': '1211',  # 暂时意义不明
        '1121': 'Inflammation',  # 炎症(包含非典型修复)-淋巴细胞性(滤泡性)宫颈炎
        '2222': 'AGC',
        '1250': 'Herpes',  # 细胞学改变符合单纯疱疹病毒
        '1113': 'Tubal_metaplasia',  # 输卵管化生
        '2212': 'AMC',  # 非典型腺细胞，倾向于子宫内膜腺细胞(AMC)
        '2211': 'AEC',  # 非典型腺细胞，倾向于宫颈管腺细胞(AEC)
        '2230': 'AIS',
        '1210': 'Trichomonas',  # 滴虫(Trichomonas)
        '0400': 'HCG',
        '1230': 'Dysbacteriosis',  # 菌群失调(Dysbacteriosis)
        '1240': 'Actinomycetes',  # 细胞形态学符合放线菌(Actinomycetes)
        '0700': 'wrong',
        '0801': 'nplus',
        '0802': 'singel',
        '0803': 'several',
        '0804': 'tens',
        '0805': 'bubble',
        '0806': 'deleted_0.0',
        '0807': 'deleted_0.100',
        '0809': 'pos',
        '0810': 'mould',
        '0811': 'nn',
        '0812': 'pp',
        '0813': 'Neg',
        '0814': 'pos_jp',
        '1300': 'Endometrium',
        '0900': 'typical_pos',
        '0902': 'nplus',
        '0903': 'cornified',
        '0904': 'superficial',
        '0905': 'atrophy',
        '0906': 'NILM',
    }

    class_to_code = {
        'ASC-H':        '2112',
        'ASC-H_0.0':    '2112',
        'ASC-H_0.100':  '2112',
        'ASC-H.contour.same':   '2112',
        'ASCH':         '2112',
        'ASC-H.delete1':'2112',
        'ASC-H.same':   '2112',
        'ASC-US.same':  '2112',
        'ASC-H.new':    '2112',
        'ASC-US':       '2111',
        'ASC-US_0.0':   '2111',
        'ASC-US_0.100': '2111',
        'ASC-US.contour.same':  '2111',
        'ASC-US.delete1':'2111',
        'ASC-US.delete11':'2111',
        'ASCUS':        '2111',
        'ASC':          '2111',
        'ASC-US':       '2111',
        'ASC-US.new':   '2111',
        'ACC-US':       '2111',
        'HSIL':         '2130',
        'HISL':         '2130',
        'HSIL.new':     '2130',
        'HSIL.delete11':'2130',
        'HSIL.delete1': '2130',
        'HSIL.same':    '2130',
        'HSIL_0.0':     '2130',
        'HSIL_0.100':   '2130',
        'nGEC':         '0200',
        'nGEC_0.0':     '0200',
        'nGEC_0.100':   '0200',
        'NGEC':         '0200',
        'ngec':         '0200',
        'LSIL':         '2120',
        'LISL':         '2120',
        'LSIL_0.0':     '2120',
        'LSIL_0.100':   '2120',
        'LSIL.new':     '2120',
        'LSIL.same':    '2120',
        'LSIL.contour.same':'2120',
        'LSIL.DELETE1': '2120',
        'LSIL.delete1': '2120',
        'others':       '3000',
        'normal':       '0000',
        'Normal':       '0000',
        'normal_0600':  '0600',  # 单个或两、三成簇可疑细胞
        '0600_0.0':     '0600',
        'Normal_0100':  '0000',  # 正常细胞 鳞状上皮来源
        'SCC':          '2140',
        'AGC_NOS':      '2213',
        'Normal_0.0':   '0000',
        'normal_0500':  '0500',
        'Normal_0500':  '0500',
        'Normal_0600':  '0600',  # 模糊可疑细胞
        'Normal_0300':  '0300',  # 正常细胞 腺来源-子宫内膜细胞
        'Normal_0400':  '0400',  # 拥挤深染细胞团(HCG)
        '1111':         '1111',
        '1111_0.0':     '1111',
        '0000':         '0000',
        '0000_0.100':   '0000',
        'IUD':          '1123',
        '1112':         '1112',
        'AGC':          '2222',
        'AEC':          '2211',
        '1121':         '1121',
        '1250':         '1250',
        '1240':         '1240',
        '1210':         '1210',
        '1123':         '1123',
        '2230':         '2230',
        '3000':         '3000',
        '2213':         '2213',
        '1113':         '1113',
        '2211':         '2211',
        '1211':         '1211',
        '2212':         '2212',
        'AIS':          '2230',
        'HCG':          '0400',
        'Uncertain':    '0000',
        'wrongA':       '0700',  # wrong anno
        'wrong':        '0700',
        'Wrong':        '0700',
        'WRONG':        '0700',
        'wrongGaodu':   '0700',
        '':             '0700',
        '0':            '0700',
        'null':         '0700',
        '0.914063632488':'0700',
        'wrongDidu':    '0700',
        '2_920':        '0700',
        'nplus':        '0801',
        'nplus_0.0':    '0801',
        'singel':       '0802',
        'several':      '0803',
        'tens':         '0804',
        '2222':         '2222',  # 非典型腺细胞(AGC),倾向于肿瘤性
        'AGC':          '2222',
        '1230':         '1230',  # 菌群失调，提示细菌性阴道病
        'bubble':       '0805',  # 泡沫
        'deleted_0.0':  '0806',
        'deleted_0.100':'0807',
        'pos':          '0809',
        'pos_jp':       '0814',
        'mould':        '0810',
        'trichomonad':  '1210',
        'nn':           '0811',
        'pp':           '0812',
        'Neg':          '0813',
        'Endometrium':  '1300',  # 子宫内膜细胞
        'typical_pos':  '0900',
        'nplus':        '0902',
        'cornified':    '0903',
        'superficial':  '0904',
        'atrophy':      '0905',
        'NILM':         '0906',
    }

    type_name = ["HSIL", "LSIL", "ASC-US", "AGC", "nGEC", "HCG", "SSC", "Candidate"]  # , "Normal"] #normal 不需要展示
    color_value = ["#ff0000", "#00ff00", "#ffff00", "#007882", "#0000ff", "#8c9664", "#8c28c8",
                  "#0a0a0a"]  # , "#00ffff"]

    zoom_dict = {'3DHistech': '20x', 'WNLO': '20x', 'SZSQ': '40x'}
    format_dict = {'3DHistech': 'mrxs', 'WNLO': 'svs', 'SZSQ': 'sdpc'}