from flask import Response


def get_response(file,style='image'):
    # https://www.iana.org/assignments/media-types/media-types.xhtml
    if style == 'image':
        return Response(file, mimetype="image/jpeg")
    if style == 'pdf':
        return Response(file, mimetype="application/pdf")
    if style == 'mp4':
        return Response(file, mimetype="file")
    return Response(file, mimetype="text/html")