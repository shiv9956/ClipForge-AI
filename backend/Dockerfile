FROM alpine:latest AS alpine
FROM n8nio/n8n:latest
 
COPY --from=alpine /sbin/apk /sbin/apk
COPY --from=alpine /usr/lib/libapk.so* /usr/lib/
COPY --from=alpine /etc/apk /etc/apk
 
USER root
RUN apk add --no-cache ffmpeg python3 ttf-dejavu fontconfig nodejs npm tini
USER node