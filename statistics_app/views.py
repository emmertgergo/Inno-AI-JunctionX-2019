from django.shortcuts import render
import os
from .models import Result, Session
from tale_app.models import Tale
from children_app.models import Child
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Avg
from JunctionX.settings import STATIC_DIR

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings

## AADTokenCredentials for multi-factor authentication
from msrestazure.azure_active_directory import AADTokenCredentials

## Required for Azure Data Lake Analytics job management
from azure.mgmt.datalake.analytics.job import DataLakeAnalyticsJobManagementClient
from azure.mgmt.datalake.analytics.job.models import JobInformation, JobState, USqlJobProperties

## Other required imports
import adal, uuid, time


def radar_factory(num_vars, frame='circle'):
    """Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle' | 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    class RadarAxes(PolarAxes):

        name = 'radar'
        # use 1 line segment to connect specified points
        RESOLUTION = 1

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)
                return {'polar': spine}
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta


def create_radar(session_id):
    data = [1, 1, 1, 1, 1, 1, 1, 1]
    results = Result.objects.filter(session__id=session_id)
    for emotion in [0, 1, 2, 3, 4, 5, 6, 7]:
        col_name = 'emotion_' + str(emotion)
        emotion_set = results.filter(content__targetemotion=emotion)

        if emotion_set:
            avg = emotion_set.aggregate(Avg(col_name))
            data[emotion] = next(iter(avg.values()))

    N = 8
    theta = radar_factory(N, frame='polygon')
    spoke_labels = ['anger', 'contempt', 'disgust', 'fear', 'happiness', 'neutral', 'sadness', 'surprise']
    fig, axes = plt.subplots(figsize=(9, 9), nrows=1, ncols=1,
                             subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)
    axes.plot(theta, data, color='b')
    axes.fill(theta, data, alpha=0.25)
    axes.set_varlabels(spoke_labels)

    # add legend relative to top-left plot
    img_path = STATIC_DIR + os.path.normpath('/statistics_app/pictures/radar_test_' + str(session_id) + '.png')
    print(img_path)
    plt.savefig(img_path, dpi=300)
    upload_blob(os.path.normpath('statistics_app/pictures/radar_test_' + str(session_id) + '.png'), img_path)
    session = Session.objects.get(pk=session_id)
    session.image_path = 'https://hackathoninnoai.blob.core.windows.net/static/statistics_app/pictures/radar_test_' + str(session_id) + '.png'
    session.save()
    return img_path


def upload_blob(path, name):
    block_blob_service = BlockBlobService(account_name='hackathoninnoai', account_key='IrZ5NR+e/OX4FcHLet9bUdurOX6O6lmRHJRfLn3x4e+hbKQ0tjoCMVi0OxiwHnnzY092cqofXfx4A48AeKfWLw==')
    block_blob_service.create_container('static')

    #Upload the CSV file to Azure cloud
    block_blob_service.create_blob_from_path(
        'static',
        path,
        name,
        content_settings=ContentSettings(content_type='application/octetstream')
                )


class ChildResult(LoginRequiredMixin, TemplateView):
    template_name = "statistics_app/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tales = []
        tale_ids = Session.objects.filter(child=Child.objects.get(pk=kwargs['child_id'])).values_list('tale', flat=True).distinct()
        for tale_id in tale_ids:
            sessions = Session.objects.filter(
                child=Child.objects.get(pk=kwargs['child_id']),
                tale__id=tale_id,
            ).order_by('date')
            tales.append([Tale.objects.get(pk=tale_id), sessions])

        # A result adatokbol kell csinalni egy listat, aztan azt meg  a contenthez hozzá kell fűzni.
        context['items'] = tales
        return context


class ChildEmotionList(LoginRequiredMixin, TemplateView):
    template_name = "statistics_app/emotion_list.html"
    emotion_enum = {0: 'anger', 1: 'contempt', 2: 'disgust', 3: 'fear', 4: 'happiness',
                    5: 'neutral', 6: 'sadness', 7: 'surprise'}

    def get_context_data(self, **kwargs):  # Ez a két sor itt ahhoz kell, hogy hozzáférjük a context-hez
        # amit belerakunka template-be
        context = super().get_context_data(**kwargs)
        all_result = Result.objects.filter(
            session__child=Child.objects.get(pk=kwargs['child_id']),
        ).order_by('-id')
        child_emotion = []
        for emotion in range(0, 8):
            emo = all_result.filter(content__targetemotion=emotion)
            if emo:
                child_emotion.append([self.emotion_enum[emotion], emo[0].image.url])
        context['items'] = child_emotion
        return context

