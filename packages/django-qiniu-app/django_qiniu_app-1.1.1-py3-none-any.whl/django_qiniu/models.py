# -*- coding: utf-8 -*-
import logging
from django.db import models
import json
from qiniu import Auth, BucketManager, AudioManager
from django.db.models.signals import post_delete, pre_save


log = logging.getLogger(__name__)


class Bucket(models.Model):
    # TODO 暂时不支持多个帐号
    name = models.SlugField(primary_key=True)
    private = models.BooleanField("是否是私有空间", default=False)
    access_key = models.SlugField(blank=False)
    secret_key = models.SlugField(blank=False)
    domain = models.CharField(blank=False, max_length=127)
    https = models.BooleanField("是否使用https", default=True)

    @property
    def qiniu_auth(self):
        if hasattr(self, "_qiniu_auth"):
            return self._qiniu_auth
        self._qiniu_auth = Auth(self.access_key, self.secret_key)
        return self._qiniu_auth

    @property
    def bucket_manager(self):
        if hasattr(self, "_bucket_manager"):
            return self._bucket_manager
        self._bucket_manager = BucketManager(self.qiniu_auth)
        return self._bucket_manager

    def __str__(self):
        return "七牛的Bucket: {}".format(self.name)


class LiveBucket(models.Model):
    """直播的空间"""
    name = models.SlugField(primary_key=True)
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE)
    push_domain = models.CharField("直播推流域名", max_length=127)
    play_domain_rtmp = models.CharField("直播推流域名rtmp", max_length=127)
    play_domain_hls = models.CharField("直播推流域名hls", max_length=127)
    play_domain_hdl = models.CharField("直播推流域名hdl", max_length=127)


class Resource(models.Model):
    """七牛的资源"""
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE)
    key = models.CharField("文件名", blank=False, max_length=127)
    # TODO size, updatetime, filetype, storagetype
    _duration = models.FloatField(null=True)

    class Meta:
        unique_together = ("bucket", "key")

    def __str__(self):
        return "七牛的资源: {}/{}".format(self.bucket.name, self.key)

    @property
    def url(self):
        if self.bucket.https:
            protocal = "https"
        else:
            protocal = "http"
        return "{}://{}/{}".format(protocal, self.bucket.domain, self.key)

    @classmethod
    def post_delete(self, sender, instance, **kwargs):
        log.info("删除七牛资源")
        log.info(instance)
        ret, info = instance.bucket.bucket_manager.delete(instance.bucket.name, instance.key)
        assert ret == {}

    @property
    def duration(self):
        if self._duration is not None:
            return self._duration
        audio_manager = AudioManager(self.bucket.qiniu_auth)
        ret, info = audio_manager.avinfo(self.url)
        self._duration = float(ret["format"]["duration"])
        self.save()
        return self._duration


class Token(models.Model):
    key = models.CharField(max_length=64, primary_key=True)
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE)
    token = models.TextField()

    @classmethod
    def pre_save(clas, sender, instance, **kwargs):
        if instance.token:
            return
        instance.token = instance.bucket.qiniu_auth.upload_token(
            instance.bucket.name, instance.key, 3600)


post_delete.connect(Resource.post_delete, sender=Resource)
pre_save.connect(Token.pre_save, sender=Token)
