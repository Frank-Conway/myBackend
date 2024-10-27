from rest_framework.response import Response
from utils.module import return_code


class RetrieveModelMixin:
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()  # 抛出异常  models.Compnay.objects.get(id=11111)
            serializer = self.get_serializer(instance)
            return Response({"code": return_code.SUCCESS, 'data': serializer.data})
        except Exception as e:
            return Response({"code": return_code.SUMMARY_ERROR, 'msg': "请求失败"})


class UpdateModelMixin:
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            if not serializer.is_valid():
                return Response({"code": return_code.FIELD_ERROR, 'msg': "error", 'detail': serializer.errors})
            self.perform_update(serializer)
            return Response({
                "code": return_code.SUCCESS,
                'msg': "success",
                'data': serializer.data
            })
        except Exception as e:
            return Response({"code": return_code.SUMMARY_ERROR, 'msg': "请求失败"})

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
