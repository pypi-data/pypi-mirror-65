from kpl_dataset import BasicType

RectangleBoxObjectDetectionDatasetDefine = {
    "path": BasicType.String,
    "content": BasicType.ByteArray,
    "contentType": BasicType.String,
    "object": [
        {"name": BasicType.String,
         "xmin": BasicType.Int,
         "xmax": BasicType.Int,
         "ymin": BasicType.Int,
         "ymax": BasicType.Int,
         "difficult": BasicType.Int,
         "score": BasicType.Float
         }
    ]
}

ClassificationDatasetDefine = {
    "path": BasicType.String,
    "content": BasicType.ByteArray,
    "contentType": BasicType.String,
    "class_name": BasicType.String,
    "class_id": BasicType.Int,
}
