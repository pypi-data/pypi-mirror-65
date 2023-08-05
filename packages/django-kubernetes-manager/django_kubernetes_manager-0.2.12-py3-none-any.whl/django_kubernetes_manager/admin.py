from django.contrib import admin
from django_kubernetes_manager.models import (TargetCluster,
    KubernetesContainer, KubernetesPodTemplate, KubernetesJob,
    KubernetesDeployment, KubernetesService, KubernetesIngress,
    KubernetesNamespace, KubernetesConfigMap, KubernetesVolume, 
    KubernetesVolumeMount)

models = [TargetCluster,
    KubernetesContainer, KubernetesPodTemplate, KubernetesJob,
    KubernetesDeployment, KubernetesService, KubernetesIngress,
    KubernetesNamespace, KubernetesConfigMap, KubernetesVolume, 
    KubernetesVolumeMount]

for model in models:
    admin.site.register(model)
