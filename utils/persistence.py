import io
import joblib


def serialize_pipeline(pipeline) -> bytes:
    buf = io.BytesIO()
    joblib.dump(pipeline, buf)
    buf.seek(0)
    return buf.read()


def deserialize_pipeline(data: bytes):
    buf = io.BytesIO(data)
    return joblib.load(buf)
