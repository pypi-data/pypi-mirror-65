#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Xiang Wang @ 2019-11-06 17:50:50

import logging
import time
from django.core.management.base import BaseCommand, CommandError
from django_qiniu.models import Bucket, Resource

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "根新所有的Resource"

    def add_arguments(self, parser):
        parser.add_argument("-timeout",
                            type=int,
                            default=120,
                            help="允许最长执行的时间")

    def handle(self, *args, **options):
        timeout = options.get("timeout")
        starttime = time.time()
        for bucket in Bucket.objects.all():
            log.info("处理{}".format(bucket))
            marker = None
            eof = False
            count = 0
            while eof is False:
                ret, eof, info = bucket.bucket_manager.list(bucket.name,
                                                            marker=marker)
                marker = ret.get("marker", None)
                count += len(ret["items"])
                keys = map(lambda x: x["key"], ret["items"])
                if Resource.objects.filter(bucket=bucket, key__in=keys).count() == len(ret["items"]):
                    log.info("处理了{}条数据".format(count))
                    continue
                for itemdata in ret["items"]:
                    if time.time() - starttime >= timeout:
                        raise CommandError(
                            "执行时间超过了设定的最大允许时间. 当前数据已保存{}条".format(count))
                    Resource.objects.get_or_create(bucket=bucket,
                                                   key=itemdata["key"])
                    time.sleep(0.001)
                log.info("处理了{}条数据".format(count))
            log.info("处理完毕")
