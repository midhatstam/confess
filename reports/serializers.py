from core.serializers import ItemMetaDataSerializer
from reports.models import ReportComment


class ReportCommentSerializer(ItemMetaDataSerializer):
    class Meta:
        model = ReportComment
        fields = '__all__'
        depth = 1
