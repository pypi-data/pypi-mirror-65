"""
Main interface for rekognition service type definitions.

Usage::

    from mypy_boto3.rekognition.type_defs import BoundingBoxTypeDef

    data: BoundingBoxTypeDef = {...}
"""
from datetime import datetime
import sys
from typing import IO, List, Union

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "BoundingBoxTypeDef",
    "ImageQualityTypeDef",
    "LandmarkTypeDef",
    "PoseTypeDef",
    "ComparedFaceTypeDef",
    "CompareFacesMatchTypeDef",
    "ComparedSourceImageFaceTypeDef",
    "CompareFacesResponseTypeDef",
    "CreateCollectionResponseTypeDef",
    "CreateProjectResponseTypeDef",
    "CreateProjectVersionResponseTypeDef",
    "CreateStreamProcessorResponseTypeDef",
    "DeleteCollectionResponseTypeDef",
    "DeleteFacesResponseTypeDef",
    "DeleteProjectResponseTypeDef",
    "DeleteProjectVersionResponseTypeDef",
    "DescribeCollectionResponseTypeDef",
    "S3ObjectTypeDef",
    "SummaryTypeDef",
    "EvaluationResultTypeDef",
    "OutputConfigTypeDef",
    "GroundTruthManifestTypeDef",
    "AssetTypeDef",
    "TestingDataTypeDef",
    "TestingDataResultTypeDef",
    "TrainingDataTypeDef",
    "TrainingDataResultTypeDef",
    "ProjectVersionDescriptionTypeDef",
    "DescribeProjectVersionsResponseTypeDef",
    "ProjectDescriptionTypeDef",
    "DescribeProjectsResponseTypeDef",
    "KinesisVideoStreamTypeDef",
    "StreamProcessorInputTypeDef",
    "KinesisDataStreamTypeDef",
    "StreamProcessorOutputTypeDef",
    "FaceSearchSettingsTypeDef",
    "StreamProcessorSettingsTypeDef",
    "DescribeStreamProcessorResponseTypeDef",
    "PointTypeDef",
    "GeometryTypeDef",
    "CustomLabelTypeDef",
    "DetectCustomLabelsResponseTypeDef",
    "AgeRangeTypeDef",
    "BeardTypeDef",
    "EmotionTypeDef",
    "EyeOpenTypeDef",
    "EyeglassesTypeDef",
    "GenderTypeDef",
    "MouthOpenTypeDef",
    "MustacheTypeDef",
    "SmileTypeDef",
    "SunglassesTypeDef",
    "FaceDetailTypeDef",
    "DetectFacesResponseTypeDef",
    "InstanceTypeDef",
    "ParentTypeDef",
    "LabelTypeDef",
    "DetectLabelsResponseTypeDef",
    "HumanLoopActivationOutputTypeDef",
    "ModerationLabelTypeDef",
    "DetectModerationLabelsResponseTypeDef",
    "DetectionFilterTypeDef",
    "RegionOfInterestTypeDef",
    "DetectTextFiltersTypeDef",
    "TextDetectionTypeDef",
    "DetectTextResponseTypeDef",
    "GetCelebrityInfoResponseTypeDef",
    "CelebrityDetailTypeDef",
    "CelebrityRecognitionTypeDef",
    "VideoMetadataTypeDef",
    "GetCelebrityRecognitionResponseTypeDef",
    "ContentModerationDetectionTypeDef",
    "GetContentModerationResponseTypeDef",
    "FaceDetectionTypeDef",
    "GetFaceDetectionResponseTypeDef",
    "FaceTypeDef",
    "FaceMatchTypeDef",
    "PersonDetailTypeDef",
    "PersonMatchTypeDef",
    "GetFaceSearchResponseTypeDef",
    "LabelDetectionTypeDef",
    "GetLabelDetectionResponseTypeDef",
    "PersonDetectionTypeDef",
    "GetPersonTrackingResponseTypeDef",
    "TextDetectionResultTypeDef",
    "GetTextDetectionResponseTypeDef",
    "HumanLoopDataAttributesTypeDef",
    "HumanLoopConfigTypeDef",
    "ImageTypeDef",
    "FaceRecordTypeDef",
    "UnindexedFaceTypeDef",
    "IndexFacesResponseTypeDef",
    "ListCollectionsResponseTypeDef",
    "ListFacesResponseTypeDef",
    "StreamProcessorTypeDef",
    "ListStreamProcessorsResponseTypeDef",
    "NotificationChannelTypeDef",
    "PaginatorConfigTypeDef",
    "CelebrityTypeDef",
    "RecognizeCelebritiesResponseTypeDef",
    "SearchFacesByImageResponseTypeDef",
    "SearchFacesResponseTypeDef",
    "StartCelebrityRecognitionResponseTypeDef",
    "StartContentModerationResponseTypeDef",
    "StartFaceDetectionResponseTypeDef",
    "StartFaceSearchResponseTypeDef",
    "StartLabelDetectionResponseTypeDef",
    "StartPersonTrackingResponseTypeDef",
    "StartProjectVersionResponseTypeDef",
    "StartTextDetectionFiltersTypeDef",
    "StartTextDetectionResponseTypeDef",
    "StopProjectVersionResponseTypeDef",
    "VideoTypeDef",
    "WaiterConfigTypeDef",
)

BoundingBoxTypeDef = TypedDict(
    "BoundingBoxTypeDef",
    {"Width": float, "Height": float, "Left": float, "Top": float},
    total=False,
)

ImageQualityTypeDef = TypedDict(
    "ImageQualityTypeDef", {"Brightness": float, "Sharpness": float}, total=False
)

LandmarkTypeDef = TypedDict(
    "LandmarkTypeDef",
    {
        "Type": Literal[
            "eyeLeft",
            "eyeRight",
            "nose",
            "mouthLeft",
            "mouthRight",
            "leftEyeBrowLeft",
            "leftEyeBrowRight",
            "leftEyeBrowUp",
            "rightEyeBrowLeft",
            "rightEyeBrowRight",
            "rightEyeBrowUp",
            "leftEyeLeft",
            "leftEyeRight",
            "leftEyeUp",
            "leftEyeDown",
            "rightEyeLeft",
            "rightEyeRight",
            "rightEyeUp",
            "rightEyeDown",
            "noseLeft",
            "noseRight",
            "mouthUp",
            "mouthDown",
            "leftPupil",
            "rightPupil",
            "upperJawlineLeft",
            "midJawlineLeft",
            "chinBottom",
            "midJawlineRight",
            "upperJawlineRight",
        ],
        "X": float,
        "Y": float,
    },
    total=False,
)

PoseTypeDef = TypedDict("PoseTypeDef", {"Roll": float, "Yaw": float, "Pitch": float}, total=False)

ComparedFaceTypeDef = TypedDict(
    "ComparedFaceTypeDef",
    {
        "BoundingBox": BoundingBoxTypeDef,
        "Confidence": float,
        "Landmarks": List[LandmarkTypeDef],
        "Pose": PoseTypeDef,
        "Quality": ImageQualityTypeDef,
    },
    total=False,
)

CompareFacesMatchTypeDef = TypedDict(
    "CompareFacesMatchTypeDef", {"Similarity": float, "Face": ComparedFaceTypeDef}, total=False
)

ComparedSourceImageFaceTypeDef = TypedDict(
    "ComparedSourceImageFaceTypeDef",
    {"BoundingBox": BoundingBoxTypeDef, "Confidence": float},
    total=False,
)

CompareFacesResponseTypeDef = TypedDict(
    "CompareFacesResponseTypeDef",
    {
        "SourceImageFace": ComparedSourceImageFaceTypeDef,
        "FaceMatches": List[CompareFacesMatchTypeDef],
        "UnmatchedFaces": List[ComparedFaceTypeDef],
        "SourceImageOrientationCorrection": Literal[
            "ROTATE_0", "ROTATE_90", "ROTATE_180", "ROTATE_270"
        ],
        "TargetImageOrientationCorrection": Literal[
            "ROTATE_0", "ROTATE_90", "ROTATE_180", "ROTATE_270"
        ],
    },
    total=False,
)

CreateCollectionResponseTypeDef = TypedDict(
    "CreateCollectionResponseTypeDef",
    {"StatusCode": int, "CollectionArn": str, "FaceModelVersion": str},
    total=False,
)

CreateProjectResponseTypeDef = TypedDict(
    "CreateProjectResponseTypeDef", {"ProjectArn": str}, total=False
)

CreateProjectVersionResponseTypeDef = TypedDict(
    "CreateProjectVersionResponseTypeDef", {"ProjectVersionArn": str}, total=False
)

CreateStreamProcessorResponseTypeDef = TypedDict(
    "CreateStreamProcessorResponseTypeDef", {"StreamProcessorArn": str}, total=False
)

DeleteCollectionResponseTypeDef = TypedDict(
    "DeleteCollectionResponseTypeDef", {"StatusCode": int}, total=False
)

DeleteFacesResponseTypeDef = TypedDict(
    "DeleteFacesResponseTypeDef", {"DeletedFaces": List[str]}, total=False
)

DeleteProjectResponseTypeDef = TypedDict(
    "DeleteProjectResponseTypeDef",
    {"Status": Literal["CREATING", "CREATED", "DELETING"]},
    total=False,
)

DeleteProjectVersionResponseTypeDef = TypedDict(
    "DeleteProjectVersionResponseTypeDef",
    {
        "Status": Literal[
            "TRAINING_IN_PROGRESS",
            "TRAINING_COMPLETED",
            "TRAINING_FAILED",
            "STARTING",
            "RUNNING",
            "FAILED",
            "STOPPING",
            "STOPPED",
            "DELETING",
        ]
    },
    total=False,
)

DescribeCollectionResponseTypeDef = TypedDict(
    "DescribeCollectionResponseTypeDef",
    {
        "FaceCount": int,
        "FaceModelVersion": str,
        "CollectionARN": str,
        "CreationTimestamp": datetime,
    },
    total=False,
)

S3ObjectTypeDef = TypedDict(
    "S3ObjectTypeDef", {"Bucket": str, "Name": str, "Version": str}, total=False
)

SummaryTypeDef = TypedDict("SummaryTypeDef", {"S3Object": S3ObjectTypeDef}, total=False)

EvaluationResultTypeDef = TypedDict(
    "EvaluationResultTypeDef", {"F1Score": float, "Summary": SummaryTypeDef}, total=False
)

OutputConfigTypeDef = TypedDict(
    "OutputConfigTypeDef", {"S3Bucket": str, "S3KeyPrefix": str}, total=False
)

GroundTruthManifestTypeDef = TypedDict(
    "GroundTruthManifestTypeDef", {"S3Object": S3ObjectTypeDef}, total=False
)

AssetTypeDef = TypedDict(
    "AssetTypeDef", {"GroundTruthManifest": GroundTruthManifestTypeDef}, total=False
)

TestingDataTypeDef = TypedDict(
    "TestingDataTypeDef", {"Assets": List[AssetTypeDef], "AutoCreate": bool}, total=False
)

TestingDataResultTypeDef = TypedDict(
    "TestingDataResultTypeDef",
    {"Input": TestingDataTypeDef, "Output": TestingDataTypeDef},
    total=False,
)

TrainingDataTypeDef = TypedDict("TrainingDataTypeDef", {"Assets": List[AssetTypeDef]}, total=False)

TrainingDataResultTypeDef = TypedDict(
    "TrainingDataResultTypeDef",
    {"Input": TrainingDataTypeDef, "Output": TrainingDataTypeDef},
    total=False,
)

ProjectVersionDescriptionTypeDef = TypedDict(
    "ProjectVersionDescriptionTypeDef",
    {
        "ProjectVersionArn": str,
        "CreationTimestamp": datetime,
        "MinInferenceUnits": int,
        "Status": Literal[
            "TRAINING_IN_PROGRESS",
            "TRAINING_COMPLETED",
            "TRAINING_FAILED",
            "STARTING",
            "RUNNING",
            "FAILED",
            "STOPPING",
            "STOPPED",
            "DELETING",
        ],
        "StatusMessage": str,
        "BillableTrainingTimeInSeconds": int,
        "TrainingEndTimestamp": datetime,
        "OutputConfig": OutputConfigTypeDef,
        "TrainingDataResult": TrainingDataResultTypeDef,
        "TestingDataResult": TestingDataResultTypeDef,
        "EvaluationResult": EvaluationResultTypeDef,
    },
    total=False,
)

DescribeProjectVersionsResponseTypeDef = TypedDict(
    "DescribeProjectVersionsResponseTypeDef",
    {"ProjectVersionDescriptions": List[ProjectVersionDescriptionTypeDef], "NextToken": str},
    total=False,
)

ProjectDescriptionTypeDef = TypedDict(
    "ProjectDescriptionTypeDef",
    {
        "ProjectArn": str,
        "CreationTimestamp": datetime,
        "Status": Literal["CREATING", "CREATED", "DELETING"],
    },
    total=False,
)

DescribeProjectsResponseTypeDef = TypedDict(
    "DescribeProjectsResponseTypeDef",
    {"ProjectDescriptions": List[ProjectDescriptionTypeDef], "NextToken": str},
    total=False,
)

KinesisVideoStreamTypeDef = TypedDict("KinesisVideoStreamTypeDef", {"Arn": str}, total=False)

StreamProcessorInputTypeDef = TypedDict(
    "StreamProcessorInputTypeDef", {"KinesisVideoStream": KinesisVideoStreamTypeDef}, total=False
)

KinesisDataStreamTypeDef = TypedDict("KinesisDataStreamTypeDef", {"Arn": str}, total=False)

StreamProcessorOutputTypeDef = TypedDict(
    "StreamProcessorOutputTypeDef", {"KinesisDataStream": KinesisDataStreamTypeDef}, total=False
)

FaceSearchSettingsTypeDef = TypedDict(
    "FaceSearchSettingsTypeDef", {"CollectionId": str, "FaceMatchThreshold": float}, total=False
)

StreamProcessorSettingsTypeDef = TypedDict(
    "StreamProcessorSettingsTypeDef", {"FaceSearch": FaceSearchSettingsTypeDef}, total=False
)

DescribeStreamProcessorResponseTypeDef = TypedDict(
    "DescribeStreamProcessorResponseTypeDef",
    {
        "Name": str,
        "StreamProcessorArn": str,
        "Status": Literal["STOPPED", "STARTING", "RUNNING", "FAILED", "STOPPING"],
        "StatusMessage": str,
        "CreationTimestamp": datetime,
        "LastUpdateTimestamp": datetime,
        "Input": StreamProcessorInputTypeDef,
        "Output": StreamProcessorOutputTypeDef,
        "RoleArn": str,
        "Settings": StreamProcessorSettingsTypeDef,
    },
    total=False,
)

PointTypeDef = TypedDict("PointTypeDef", {"X": float, "Y": float}, total=False)

GeometryTypeDef = TypedDict(
    "GeometryTypeDef",
    {"BoundingBox": BoundingBoxTypeDef, "Polygon": List[PointTypeDef]},
    total=False,
)

CustomLabelTypeDef = TypedDict(
    "CustomLabelTypeDef",
    {"Name": str, "Confidence": float, "Geometry": GeometryTypeDef},
    total=False,
)

DetectCustomLabelsResponseTypeDef = TypedDict(
    "DetectCustomLabelsResponseTypeDef", {"CustomLabels": List[CustomLabelTypeDef]}, total=False
)

AgeRangeTypeDef = TypedDict("AgeRangeTypeDef", {"Low": int, "High": int}, total=False)

BeardTypeDef = TypedDict("BeardTypeDef", {"Value": bool, "Confidence": float}, total=False)

EmotionTypeDef = TypedDict(
    "EmotionTypeDef",
    {
        "Type": Literal[
            "HAPPY", "SAD", "ANGRY", "CONFUSED", "DISGUSTED", "SURPRISED", "CALM", "UNKNOWN", "FEAR"
        ],
        "Confidence": float,
    },
    total=False,
)

EyeOpenTypeDef = TypedDict("EyeOpenTypeDef", {"Value": bool, "Confidence": float}, total=False)

EyeglassesTypeDef = TypedDict(
    "EyeglassesTypeDef", {"Value": bool, "Confidence": float}, total=False
)

GenderTypeDef = TypedDict(
    "GenderTypeDef", {"Value": Literal["Male", "Female"], "Confidence": float}, total=False
)

MouthOpenTypeDef = TypedDict("MouthOpenTypeDef", {"Value": bool, "Confidence": float}, total=False)

MustacheTypeDef = TypedDict("MustacheTypeDef", {"Value": bool, "Confidence": float}, total=False)

SmileTypeDef = TypedDict("SmileTypeDef", {"Value": bool, "Confidence": float}, total=False)

SunglassesTypeDef = TypedDict(
    "SunglassesTypeDef", {"Value": bool, "Confidence": float}, total=False
)

FaceDetailTypeDef = TypedDict(
    "FaceDetailTypeDef",
    {
        "BoundingBox": BoundingBoxTypeDef,
        "AgeRange": AgeRangeTypeDef,
        "Smile": SmileTypeDef,
        "Eyeglasses": EyeglassesTypeDef,
        "Sunglasses": SunglassesTypeDef,
        "Gender": GenderTypeDef,
        "Beard": BeardTypeDef,
        "Mustache": MustacheTypeDef,
        "EyesOpen": EyeOpenTypeDef,
        "MouthOpen": MouthOpenTypeDef,
        "Emotions": List[EmotionTypeDef],
        "Landmarks": List[LandmarkTypeDef],
        "Pose": PoseTypeDef,
        "Quality": ImageQualityTypeDef,
        "Confidence": float,
    },
    total=False,
)

DetectFacesResponseTypeDef = TypedDict(
    "DetectFacesResponseTypeDef",
    {
        "FaceDetails": List[FaceDetailTypeDef],
        "OrientationCorrection": Literal["ROTATE_0", "ROTATE_90", "ROTATE_180", "ROTATE_270"],
    },
    total=False,
)

InstanceTypeDef = TypedDict(
    "InstanceTypeDef", {"BoundingBox": BoundingBoxTypeDef, "Confidence": float}, total=False
)

ParentTypeDef = TypedDict("ParentTypeDef", {"Name": str}, total=False)

LabelTypeDef = TypedDict(
    "LabelTypeDef",
    {
        "Name": str,
        "Confidence": float,
        "Instances": List[InstanceTypeDef],
        "Parents": List[ParentTypeDef],
    },
    total=False,
)

DetectLabelsResponseTypeDef = TypedDict(
    "DetectLabelsResponseTypeDef",
    {
        "Labels": List[LabelTypeDef],
        "OrientationCorrection": Literal["ROTATE_0", "ROTATE_90", "ROTATE_180", "ROTATE_270"],
        "LabelModelVersion": str,
    },
    total=False,
)

HumanLoopActivationOutputTypeDef = TypedDict(
    "HumanLoopActivationOutputTypeDef",
    {
        "HumanLoopArn": str,
        "HumanLoopActivationReasons": List[str],
        "HumanLoopActivationConditionsEvaluationResults": str,
    },
    total=False,
)

ModerationLabelTypeDef = TypedDict(
    "ModerationLabelTypeDef", {"Confidence": float, "Name": str, "ParentName": str}, total=False
)

DetectModerationLabelsResponseTypeDef = TypedDict(
    "DetectModerationLabelsResponseTypeDef",
    {
        "ModerationLabels": List[ModerationLabelTypeDef],
        "ModerationModelVersion": str,
        "HumanLoopActivationOutput": HumanLoopActivationOutputTypeDef,
    },
    total=False,
)

DetectionFilterTypeDef = TypedDict(
    "DetectionFilterTypeDef",
    {"MinConfidence": float, "MinBoundingBoxHeight": float, "MinBoundingBoxWidth": float},
    total=False,
)

RegionOfInterestTypeDef = TypedDict(
    "RegionOfInterestTypeDef", {"BoundingBox": BoundingBoxTypeDef}, total=False
)

DetectTextFiltersTypeDef = TypedDict(
    "DetectTextFiltersTypeDef",
    {"WordFilter": DetectionFilterTypeDef, "RegionsOfInterest": List[RegionOfInterestTypeDef]},
    total=False,
)

TextDetectionTypeDef = TypedDict(
    "TextDetectionTypeDef",
    {
        "DetectedText": str,
        "Type": Literal["LINE", "WORD"],
        "Id": int,
        "ParentId": int,
        "Confidence": float,
        "Geometry": GeometryTypeDef,
    },
    total=False,
)

DetectTextResponseTypeDef = TypedDict(
    "DetectTextResponseTypeDef",
    {"TextDetections": List[TextDetectionTypeDef], "TextModelVersion": str},
    total=False,
)

GetCelebrityInfoResponseTypeDef = TypedDict(
    "GetCelebrityInfoResponseTypeDef", {"Urls": List[str], "Name": str}, total=False
)

CelebrityDetailTypeDef = TypedDict(
    "CelebrityDetailTypeDef",
    {
        "Urls": List[str],
        "Name": str,
        "Id": str,
        "Confidence": float,
        "BoundingBox": BoundingBoxTypeDef,
        "Face": FaceDetailTypeDef,
    },
    total=False,
)

CelebrityRecognitionTypeDef = TypedDict(
    "CelebrityRecognitionTypeDef",
    {"Timestamp": int, "Celebrity": CelebrityDetailTypeDef},
    total=False,
)

VideoMetadataTypeDef = TypedDict(
    "VideoMetadataTypeDef",
    {
        "Codec": str,
        "DurationMillis": int,
        "Format": str,
        "FrameRate": float,
        "FrameHeight": int,
        "FrameWidth": int,
    },
    total=False,
)

GetCelebrityRecognitionResponseTypeDef = TypedDict(
    "GetCelebrityRecognitionResponseTypeDef",
    {
        "JobStatus": Literal["IN_PROGRESS", "SUCCEEDED", "FAILED"],
        "StatusMessage": str,
        "VideoMetadata": VideoMetadataTypeDef,
        "NextToken": str,
        "Celebrities": List[CelebrityRecognitionTypeDef],
    },
    total=False,
)

ContentModerationDetectionTypeDef = TypedDict(
    "ContentModerationDetectionTypeDef",
    {"Timestamp": int, "ModerationLabel": ModerationLabelTypeDef},
    total=False,
)

GetContentModerationResponseTypeDef = TypedDict(
    "GetContentModerationResponseTypeDef",
    {
        "JobStatus": Literal["IN_PROGRESS", "SUCCEEDED", "FAILED"],
        "StatusMessage": str,
        "VideoMetadata": VideoMetadataTypeDef,
        "ModerationLabels": List[ContentModerationDetectionTypeDef],
        "NextToken": str,
        "ModerationModelVersion": str,
    },
    total=False,
)

FaceDetectionTypeDef = TypedDict(
    "FaceDetectionTypeDef", {"Timestamp": int, "Face": FaceDetailTypeDef}, total=False
)

GetFaceDetectionResponseTypeDef = TypedDict(
    "GetFaceDetectionResponseTypeDef",
    {
        "JobStatus": Literal["IN_PROGRESS", "SUCCEEDED", "FAILED"],
        "StatusMessage": str,
        "VideoMetadata": VideoMetadataTypeDef,
        "NextToken": str,
        "Faces": List[FaceDetectionTypeDef],
    },
    total=False,
)

FaceTypeDef = TypedDict(
    "FaceTypeDef",
    {
        "FaceId": str,
        "BoundingBox": BoundingBoxTypeDef,
        "ImageId": str,
        "ExternalImageId": str,
        "Confidence": float,
    },
    total=False,
)

FaceMatchTypeDef = TypedDict(
    "FaceMatchTypeDef", {"Similarity": float, "Face": FaceTypeDef}, total=False
)

PersonDetailTypeDef = TypedDict(
    "PersonDetailTypeDef",
    {"Index": int, "BoundingBox": BoundingBoxTypeDef, "Face": FaceDetailTypeDef},
    total=False,
)

PersonMatchTypeDef = TypedDict(
    "PersonMatchTypeDef",
    {"Timestamp": int, "Person": PersonDetailTypeDef, "FaceMatches": List[FaceMatchTypeDef]},
    total=False,
)

GetFaceSearchResponseTypeDef = TypedDict(
    "GetFaceSearchResponseTypeDef",
    {
        "JobStatus": Literal["IN_PROGRESS", "SUCCEEDED", "FAILED"],
        "StatusMessage": str,
        "NextToken": str,
        "VideoMetadata": VideoMetadataTypeDef,
        "Persons": List[PersonMatchTypeDef],
    },
    total=False,
)

LabelDetectionTypeDef = TypedDict(
    "LabelDetectionTypeDef", {"Timestamp": int, "Label": LabelTypeDef}, total=False
)

GetLabelDetectionResponseTypeDef = TypedDict(
    "GetLabelDetectionResponseTypeDef",
    {
        "JobStatus": Literal["IN_PROGRESS", "SUCCEEDED", "FAILED"],
        "StatusMessage": str,
        "VideoMetadata": VideoMetadataTypeDef,
        "NextToken": str,
        "Labels": List[LabelDetectionTypeDef],
        "LabelModelVersion": str,
    },
    total=False,
)

PersonDetectionTypeDef = TypedDict(
    "PersonDetectionTypeDef", {"Timestamp": int, "Person": PersonDetailTypeDef}, total=False
)

GetPersonTrackingResponseTypeDef = TypedDict(
    "GetPersonTrackingResponseTypeDef",
    {
        "JobStatus": Literal["IN_PROGRESS", "SUCCEEDED", "FAILED"],
        "StatusMessage": str,
        "VideoMetadata": VideoMetadataTypeDef,
        "NextToken": str,
        "Persons": List[PersonDetectionTypeDef],
    },
    total=False,
)

TextDetectionResultTypeDef = TypedDict(
    "TextDetectionResultTypeDef",
    {"Timestamp": int, "TextDetection": TextDetectionTypeDef},
    total=False,
)

GetTextDetectionResponseTypeDef = TypedDict(
    "GetTextDetectionResponseTypeDef",
    {
        "JobStatus": Literal["IN_PROGRESS", "SUCCEEDED", "FAILED"],
        "StatusMessage": str,
        "VideoMetadata": VideoMetadataTypeDef,
        "TextDetections": List[TextDetectionResultTypeDef],
        "NextToken": str,
        "TextModelVersion": str,
    },
    total=False,
)

HumanLoopDataAttributesTypeDef = TypedDict(
    "HumanLoopDataAttributesTypeDef",
    {
        "ContentClassifiers": List[
            Literal["FreeOfPersonallyIdentifiableInformation", "FreeOfAdultContent"]
        ]
    },
    total=False,
)

_RequiredHumanLoopConfigTypeDef = TypedDict(
    "_RequiredHumanLoopConfigTypeDef", {"HumanLoopName": str, "FlowDefinitionArn": str}
)
_OptionalHumanLoopConfigTypeDef = TypedDict(
    "_OptionalHumanLoopConfigTypeDef",
    {"DataAttributes": HumanLoopDataAttributesTypeDef},
    total=False,
)


class HumanLoopConfigTypeDef(_RequiredHumanLoopConfigTypeDef, _OptionalHumanLoopConfigTypeDef):
    pass


ImageTypeDef = TypedDict(
    "ImageTypeDef", {"Bytes": Union[bytes, IO], "S3Object": S3ObjectTypeDef}, total=False
)

FaceRecordTypeDef = TypedDict(
    "FaceRecordTypeDef", {"Face": FaceTypeDef, "FaceDetail": FaceDetailTypeDef}, total=False
)

UnindexedFaceTypeDef = TypedDict(
    "UnindexedFaceTypeDef",
    {
        "Reasons": List[
            Literal[
                "EXCEEDS_MAX_FACES",
                "EXTREME_POSE",
                "LOW_BRIGHTNESS",
                "LOW_SHARPNESS",
                "LOW_CONFIDENCE",
                "SMALL_BOUNDING_BOX",
                "LOW_FACE_QUALITY",
            ]
        ],
        "FaceDetail": FaceDetailTypeDef,
    },
    total=False,
)

IndexFacesResponseTypeDef = TypedDict(
    "IndexFacesResponseTypeDef",
    {
        "FaceRecords": List[FaceRecordTypeDef],
        "OrientationCorrection": Literal["ROTATE_0", "ROTATE_90", "ROTATE_180", "ROTATE_270"],
        "FaceModelVersion": str,
        "UnindexedFaces": List[UnindexedFaceTypeDef],
    },
    total=False,
)

ListCollectionsResponseTypeDef = TypedDict(
    "ListCollectionsResponseTypeDef",
    {"CollectionIds": List[str], "NextToken": str, "FaceModelVersions": List[str]},
    total=False,
)

ListFacesResponseTypeDef = TypedDict(
    "ListFacesResponseTypeDef",
    {"Faces": List[FaceTypeDef], "NextToken": str, "FaceModelVersion": str},
    total=False,
)

StreamProcessorTypeDef = TypedDict(
    "StreamProcessorTypeDef",
    {"Name": str, "Status": Literal["STOPPED", "STARTING", "RUNNING", "FAILED", "STOPPING"]},
    total=False,
)

ListStreamProcessorsResponseTypeDef = TypedDict(
    "ListStreamProcessorsResponseTypeDef",
    {"NextToken": str, "StreamProcessors": List[StreamProcessorTypeDef]},
    total=False,
)

NotificationChannelTypeDef = TypedDict(
    "NotificationChannelTypeDef", {"SNSTopicArn": str, "RoleArn": str}
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

CelebrityTypeDef = TypedDict(
    "CelebrityTypeDef",
    {
        "Urls": List[str],
        "Name": str,
        "Id": str,
        "Face": ComparedFaceTypeDef,
        "MatchConfidence": float,
    },
    total=False,
)

RecognizeCelebritiesResponseTypeDef = TypedDict(
    "RecognizeCelebritiesResponseTypeDef",
    {
        "CelebrityFaces": List[CelebrityTypeDef],
        "UnrecognizedFaces": List[ComparedFaceTypeDef],
        "OrientationCorrection": Literal["ROTATE_0", "ROTATE_90", "ROTATE_180", "ROTATE_270"],
    },
    total=False,
)

SearchFacesByImageResponseTypeDef = TypedDict(
    "SearchFacesByImageResponseTypeDef",
    {
        "SearchedFaceBoundingBox": BoundingBoxTypeDef,
        "SearchedFaceConfidence": float,
        "FaceMatches": List[FaceMatchTypeDef],
        "FaceModelVersion": str,
    },
    total=False,
)

SearchFacesResponseTypeDef = TypedDict(
    "SearchFacesResponseTypeDef",
    {"SearchedFaceId": str, "FaceMatches": List[FaceMatchTypeDef], "FaceModelVersion": str},
    total=False,
)

StartCelebrityRecognitionResponseTypeDef = TypedDict(
    "StartCelebrityRecognitionResponseTypeDef", {"JobId": str}, total=False
)

StartContentModerationResponseTypeDef = TypedDict(
    "StartContentModerationResponseTypeDef", {"JobId": str}, total=False
)

StartFaceDetectionResponseTypeDef = TypedDict(
    "StartFaceDetectionResponseTypeDef", {"JobId": str}, total=False
)

StartFaceSearchResponseTypeDef = TypedDict(
    "StartFaceSearchResponseTypeDef", {"JobId": str}, total=False
)

StartLabelDetectionResponseTypeDef = TypedDict(
    "StartLabelDetectionResponseTypeDef", {"JobId": str}, total=False
)

StartPersonTrackingResponseTypeDef = TypedDict(
    "StartPersonTrackingResponseTypeDef", {"JobId": str}, total=False
)

StartProjectVersionResponseTypeDef = TypedDict(
    "StartProjectVersionResponseTypeDef",
    {
        "Status": Literal[
            "TRAINING_IN_PROGRESS",
            "TRAINING_COMPLETED",
            "TRAINING_FAILED",
            "STARTING",
            "RUNNING",
            "FAILED",
            "STOPPING",
            "STOPPED",
            "DELETING",
        ]
    },
    total=False,
)

StartTextDetectionFiltersTypeDef = TypedDict(
    "StartTextDetectionFiltersTypeDef",
    {"WordFilter": DetectionFilterTypeDef, "RegionsOfInterest": List[RegionOfInterestTypeDef]},
    total=False,
)

StartTextDetectionResponseTypeDef = TypedDict(
    "StartTextDetectionResponseTypeDef", {"JobId": str}, total=False
)

StopProjectVersionResponseTypeDef = TypedDict(
    "StopProjectVersionResponseTypeDef",
    {
        "Status": Literal[
            "TRAINING_IN_PROGRESS",
            "TRAINING_COMPLETED",
            "TRAINING_FAILED",
            "STARTING",
            "RUNNING",
            "FAILED",
            "STOPPING",
            "STOPPED",
            "DELETING",
        ]
    },
    total=False,
)

VideoTypeDef = TypedDict("VideoTypeDef", {"S3Object": S3ObjectTypeDef}, total=False)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef", {"Delay": int, "MaxAttempts": int}, total=False
)
