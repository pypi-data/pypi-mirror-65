from django.db.models import Model


class ModelView(Model):

    def save(self, *args, **kwargs):
        raise UserWarning(
            "Cannot save model view. The model is a database view")

    def save_base(self, *args, **kwargs):
        raise UserWarning(
            "Cannot save model view. The model is a database view")

    def delete(self, *args, **kwargs):
        raise UserWarning(
            "Cannot delete model view. The model is a database view")
