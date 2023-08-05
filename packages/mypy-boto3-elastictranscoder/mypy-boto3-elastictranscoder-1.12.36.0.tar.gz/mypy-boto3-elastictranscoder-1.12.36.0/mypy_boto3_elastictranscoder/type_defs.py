"""
Main interface for elastictranscoder service type definitions.

Usage::

    from mypy_boto3.elastictranscoder.type_defs import AudioCodecOptionsTypeDef

    data: AudioCodecOptionsTypeDef = {...}
"""
import sys
from typing import Dict, List

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AudioCodecOptionsTypeDef",
    "AudioParametersTypeDef",
    "EncryptionTypeDef",
    "CaptionFormatTypeDef",
    "CaptionSourceTypeDef",
    "CaptionsTypeDef",
    "TimeSpanTypeDef",
    "ClipTypeDef",
    "ArtworkTypeDef",
    "JobAlbumArtTypeDef",
    "JobWatermarkTypeDef",
    "CreateJobOutputTypeDef",
    "HlsContentProtectionTypeDef",
    "PlayReadyDrmTypeDef",
    "CreateJobPlaylistTypeDef",
    "DetectedPropertiesTypeDef",
    "InputCaptionsTypeDef",
    "JobInputTypeDef",
    "JobOutputTypeDef",
    "PlaylistTypeDef",
    "TimingTypeDef",
    "JobTypeDef",
    "CreateJobResponseTypeDef",
    "NotificationsTypeDef",
    "PermissionTypeDef",
    "PipelineOutputConfigTypeDef",
    "PipelineTypeDef",
    "WarningTypeDef",
    "CreatePipelineResponseTypeDef",
    "ThumbnailsTypeDef",
    "PresetWatermarkTypeDef",
    "VideoParametersTypeDef",
    "PresetTypeDef",
    "CreatePresetResponseTypeDef",
    "ListJobsByPipelineResponseTypeDef",
    "ListJobsByStatusResponseTypeDef",
    "ListPipelinesResponseTypeDef",
    "ListPresetsResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ReadJobResponseTypeDef",
    "ReadPipelineResponseTypeDef",
    "ReadPresetResponseTypeDef",
    "TestRoleResponseTypeDef",
    "UpdatePipelineNotificationsResponseTypeDef",
    "UpdatePipelineResponseTypeDef",
    "UpdatePipelineStatusResponseTypeDef",
    "WaiterConfigTypeDef",
)

AudioCodecOptionsTypeDef = TypedDict(
    "AudioCodecOptionsTypeDef",
    {"Profile": str, "BitDepth": str, "BitOrder": str, "Signed": str},
    total=False,
)

AudioParametersTypeDef = TypedDict(
    "AudioParametersTypeDef",
    {
        "Codec": str,
        "SampleRate": str,
        "BitRate": str,
        "Channels": str,
        "AudioPackingMode": str,
        "CodecOptions": AudioCodecOptionsTypeDef,
    },
    total=False,
)

EncryptionTypeDef = TypedDict(
    "EncryptionTypeDef",
    {"Mode": str, "Key": str, "KeyMd5": str, "InitializationVector": str},
    total=False,
)

CaptionFormatTypeDef = TypedDict(
    "CaptionFormatTypeDef",
    {"Format": str, "Pattern": str, "Encryption": EncryptionTypeDef},
    total=False,
)

CaptionSourceTypeDef = TypedDict(
    "CaptionSourceTypeDef",
    {"Key": str, "Language": str, "TimeOffset": str, "Label": str, "Encryption": EncryptionTypeDef},
    total=False,
)

CaptionsTypeDef = TypedDict(
    "CaptionsTypeDef",
    {
        "MergePolicy": str,
        "CaptionSources": List[CaptionSourceTypeDef],
        "CaptionFormats": List[CaptionFormatTypeDef],
    },
    total=False,
)

TimeSpanTypeDef = TypedDict("TimeSpanTypeDef", {"StartTime": str, "Duration": str}, total=False)

ClipTypeDef = TypedDict("ClipTypeDef", {"TimeSpan": TimeSpanTypeDef}, total=False)

ArtworkTypeDef = TypedDict(
    "ArtworkTypeDef",
    {
        "InputKey": str,
        "MaxWidth": str,
        "MaxHeight": str,
        "SizingPolicy": str,
        "PaddingPolicy": str,
        "AlbumArtFormat": str,
        "Encryption": EncryptionTypeDef,
    },
    total=False,
)

JobAlbumArtTypeDef = TypedDict(
    "JobAlbumArtTypeDef", {"MergePolicy": str, "Artwork": List[ArtworkTypeDef]}, total=False
)

JobWatermarkTypeDef = TypedDict(
    "JobWatermarkTypeDef",
    {"PresetWatermarkId": str, "InputKey": str, "Encryption": EncryptionTypeDef},
    total=False,
)

CreateJobOutputTypeDef = TypedDict(
    "CreateJobOutputTypeDef",
    {
        "Key": str,
        "ThumbnailPattern": str,
        "ThumbnailEncryption": EncryptionTypeDef,
        "Rotate": str,
        "PresetId": str,
        "SegmentDuration": str,
        "Watermarks": List[JobWatermarkTypeDef],
        "AlbumArt": JobAlbumArtTypeDef,
        "Composition": List[ClipTypeDef],
        "Captions": CaptionsTypeDef,
        "Encryption": EncryptionTypeDef,
    },
    total=False,
)

HlsContentProtectionTypeDef = TypedDict(
    "HlsContentProtectionTypeDef",
    {
        "Method": str,
        "Key": str,
        "KeyMd5": str,
        "InitializationVector": str,
        "LicenseAcquisitionUrl": str,
        "KeyStoragePolicy": str,
    },
    total=False,
)

PlayReadyDrmTypeDef = TypedDict(
    "PlayReadyDrmTypeDef",
    {
        "Format": str,
        "Key": str,
        "KeyMd5": str,
        "KeyId": str,
        "InitializationVector": str,
        "LicenseAcquisitionUrl": str,
    },
    total=False,
)

CreateJobPlaylistTypeDef = TypedDict(
    "CreateJobPlaylistTypeDef",
    {
        "Name": str,
        "Format": str,
        "OutputKeys": List[str],
        "HlsContentProtection": HlsContentProtectionTypeDef,
        "PlayReadyDrm": PlayReadyDrmTypeDef,
    },
    total=False,
)

DetectedPropertiesTypeDef = TypedDict(
    "DetectedPropertiesTypeDef",
    {"Width": int, "Height": int, "FrameRate": str, "FileSize": int, "DurationMillis": int},
    total=False,
)

InputCaptionsTypeDef = TypedDict(
    "InputCaptionsTypeDef",
    {"MergePolicy": str, "CaptionSources": List[CaptionSourceTypeDef]},
    total=False,
)

JobInputTypeDef = TypedDict(
    "JobInputTypeDef",
    {
        "Key": str,
        "FrameRate": str,
        "Resolution": str,
        "AspectRatio": str,
        "Interlaced": str,
        "Container": str,
        "Encryption": EncryptionTypeDef,
        "TimeSpan": TimeSpanTypeDef,
        "InputCaptions": InputCaptionsTypeDef,
        "DetectedProperties": DetectedPropertiesTypeDef,
    },
    total=False,
)

JobOutputTypeDef = TypedDict(
    "JobOutputTypeDef",
    {
        "Id": str,
        "Key": str,
        "ThumbnailPattern": str,
        "ThumbnailEncryption": EncryptionTypeDef,
        "Rotate": str,
        "PresetId": str,
        "SegmentDuration": str,
        "Status": str,
        "StatusDetail": str,
        "Duration": int,
        "Width": int,
        "Height": int,
        "FrameRate": str,
        "FileSize": int,
        "DurationMillis": int,
        "Watermarks": List[JobWatermarkTypeDef],
        "AlbumArt": JobAlbumArtTypeDef,
        "Composition": List[ClipTypeDef],
        "Captions": CaptionsTypeDef,
        "Encryption": EncryptionTypeDef,
        "AppliedColorSpaceConversion": str,
    },
    total=False,
)

PlaylistTypeDef = TypedDict(
    "PlaylistTypeDef",
    {
        "Name": str,
        "Format": str,
        "OutputKeys": List[str],
        "HlsContentProtection": HlsContentProtectionTypeDef,
        "PlayReadyDrm": PlayReadyDrmTypeDef,
        "Status": str,
        "StatusDetail": str,
    },
    total=False,
)

TimingTypeDef = TypedDict(
    "TimingTypeDef",
    {"SubmitTimeMillis": int, "StartTimeMillis": int, "FinishTimeMillis": int},
    total=False,
)

JobTypeDef = TypedDict(
    "JobTypeDef",
    {
        "Id": str,
        "Arn": str,
        "PipelineId": str,
        "Input": JobInputTypeDef,
        "Inputs": List[JobInputTypeDef],
        "Output": JobOutputTypeDef,
        "Outputs": List[JobOutputTypeDef],
        "OutputKeyPrefix": str,
        "Playlists": List[PlaylistTypeDef],
        "Status": str,
        "UserMetadata": Dict[str, str],
        "Timing": TimingTypeDef,
    },
    total=False,
)

CreateJobResponseTypeDef = TypedDict("CreateJobResponseTypeDef", {"Job": JobTypeDef}, total=False)

NotificationsTypeDef = TypedDict(
    "NotificationsTypeDef",
    {"Progressing": str, "Completed": str, "Warning": str, "Error": str},
    total=False,
)

PermissionTypeDef = TypedDict(
    "PermissionTypeDef", {"GranteeType": str, "Grantee": str, "Access": List[str]}, total=False
)

PipelineOutputConfigTypeDef = TypedDict(
    "PipelineOutputConfigTypeDef",
    {"Bucket": str, "StorageClass": str, "Permissions": List[PermissionTypeDef]},
    total=False,
)

PipelineTypeDef = TypedDict(
    "PipelineTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
        "Status": str,
        "InputBucket": str,
        "OutputBucket": str,
        "Role": str,
        "AwsKmsKeyArn": str,
        "Notifications": NotificationsTypeDef,
        "ContentConfig": PipelineOutputConfigTypeDef,
        "ThumbnailConfig": PipelineOutputConfigTypeDef,
    },
    total=False,
)

WarningTypeDef = TypedDict("WarningTypeDef", {"Code": str, "Message": str}, total=False)

CreatePipelineResponseTypeDef = TypedDict(
    "CreatePipelineResponseTypeDef",
    {"Pipeline": PipelineTypeDef, "Warnings": List[WarningTypeDef]},
    total=False,
)

ThumbnailsTypeDef = TypedDict(
    "ThumbnailsTypeDef",
    {
        "Format": str,
        "Interval": str,
        "Resolution": str,
        "AspectRatio": str,
        "MaxWidth": str,
        "MaxHeight": str,
        "SizingPolicy": str,
        "PaddingPolicy": str,
    },
    total=False,
)

PresetWatermarkTypeDef = TypedDict(
    "PresetWatermarkTypeDef",
    {
        "Id": str,
        "MaxWidth": str,
        "MaxHeight": str,
        "SizingPolicy": str,
        "HorizontalAlign": str,
        "HorizontalOffset": str,
        "VerticalAlign": str,
        "VerticalOffset": str,
        "Opacity": str,
        "Target": str,
    },
    total=False,
)

VideoParametersTypeDef = TypedDict(
    "VideoParametersTypeDef",
    {
        "Codec": str,
        "CodecOptions": Dict[str, str],
        "KeyframesMaxDist": str,
        "FixedGOP": str,
        "BitRate": str,
        "FrameRate": str,
        "MaxFrameRate": str,
        "Resolution": str,
        "AspectRatio": str,
        "MaxWidth": str,
        "MaxHeight": str,
        "DisplayAspectRatio": str,
        "SizingPolicy": str,
        "PaddingPolicy": str,
        "Watermarks": List[PresetWatermarkTypeDef],
    },
    total=False,
)

PresetTypeDef = TypedDict(
    "PresetTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
        "Description": str,
        "Container": str,
        "Audio": AudioParametersTypeDef,
        "Video": VideoParametersTypeDef,
        "Thumbnails": ThumbnailsTypeDef,
        "Type": str,
    },
    total=False,
)

CreatePresetResponseTypeDef = TypedDict(
    "CreatePresetResponseTypeDef", {"Preset": PresetTypeDef, "Warning": str}, total=False
)

ListJobsByPipelineResponseTypeDef = TypedDict(
    "ListJobsByPipelineResponseTypeDef",
    {"Jobs": List[JobTypeDef], "NextPageToken": str},
    total=False,
)

ListJobsByStatusResponseTypeDef = TypedDict(
    "ListJobsByStatusResponseTypeDef", {"Jobs": List[JobTypeDef], "NextPageToken": str}, total=False
)

ListPipelinesResponseTypeDef = TypedDict(
    "ListPipelinesResponseTypeDef",
    {"Pipelines": List[PipelineTypeDef], "NextPageToken": str},
    total=False,
)

ListPresetsResponseTypeDef = TypedDict(
    "ListPresetsResponseTypeDef",
    {"Presets": List[PresetTypeDef], "NextPageToken": str},
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

ReadJobResponseTypeDef = TypedDict("ReadJobResponseTypeDef", {"Job": JobTypeDef}, total=False)

ReadPipelineResponseTypeDef = TypedDict(
    "ReadPipelineResponseTypeDef",
    {"Pipeline": PipelineTypeDef, "Warnings": List[WarningTypeDef]},
    total=False,
)

ReadPresetResponseTypeDef = TypedDict(
    "ReadPresetResponseTypeDef", {"Preset": PresetTypeDef}, total=False
)

TestRoleResponseTypeDef = TypedDict(
    "TestRoleResponseTypeDef", {"Success": str, "Messages": List[str]}, total=False
)

UpdatePipelineNotificationsResponseTypeDef = TypedDict(
    "UpdatePipelineNotificationsResponseTypeDef", {"Pipeline": PipelineTypeDef}, total=False
)

UpdatePipelineResponseTypeDef = TypedDict(
    "UpdatePipelineResponseTypeDef",
    {"Pipeline": PipelineTypeDef, "Warnings": List[WarningTypeDef]},
    total=False,
)

UpdatePipelineStatusResponseTypeDef = TypedDict(
    "UpdatePipelineStatusResponseTypeDef", {"Pipeline": PipelineTypeDef}, total=False
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef", {"Delay": int, "MaxAttempts": int}, total=False
)
