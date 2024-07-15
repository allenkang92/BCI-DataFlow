from sklearn.decomposition import FastICA

def ica_artifact_removal(data, n_components=None):
    ica = FastICA(n_components=n_components, random_state=0)
    S_ = ica.fit_transform(data.T)
    # 여기에 아티팩트 성분을 식별하고 제거하는 로직 추가
    return S_.T