from django.contrib import admin
from django.urls import include, path

from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter

from . import views

app_name = "katka_core"

router = routers.SimpleRouter()
router.register("teams", views.TeamViewSet, basename="teams")
router.register("projects", views.ProjectViewSet, basename="projects")
router.register("applications", views.ApplicationViewSet, basename="applications")
router.register("credentials", views.CredentialViewSet, basename="credentials")
router.register("scm-services", views.SCMServiceViewSet, basename="scm-services")
router.register("scm-repositories", views.SCMRepositoryViewSet, basename="scm-repositories")
router.register("scm-pipeline-runs", views.SCMPipelineRunViewSet, basename="scm-pipeline-runs")
router.register("queued-scm-pipeline-runs", views.QueuedSCMPipelineRunViewSet, basename="queued-scm-pipeline-runs")
router.register("scm-step-runs", views.SCMStepRunViewSet, basename="scm-step-runs")
router.register("scm-releases", views.SCMReleaseViewSet, basename="scm-releases")
router.register("update-scm-step-run", views.SCMStepRunUpdateStatusView, basename="update-scm-step-run")
router.register(
    "append-build-info-scm-step-run", views.SCMStepRunAppendBuildInfoView, basename="append-build-info-scm-step-run"
)

secrets_router = NestedSimpleRouter(router, "credentials", lookup="credentials")
secrets_router.register("secrets", views.CredentialSecretsViewSet, basename="secrets")

app_metadata_router = NestedSimpleRouter(router, "applications", lookup="applications")
app_metadata_router.register("metadata", views.ApplicationMetadataViewSet, basename="metadata")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("", include(secrets_router.urls)),
    path("", include(app_metadata_router.urls)),
]
