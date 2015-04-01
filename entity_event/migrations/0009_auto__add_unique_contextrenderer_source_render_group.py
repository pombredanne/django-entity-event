# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'RenderGroup'
        db.delete_table(u'entity_event_rendergroup')

        # Adding model 'RenderingStyle'
        db.create_table(u'entity_event_renderingstyle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('display_name', self.gf('django.db.models.fields.CharField')(default='', max_length=64)),
        ))
        db.send_create_signal(u'entity_event', ['RenderingStyle'])

        # Deleting field 'ContextRenderer.render_group'
        db.delete_column(u'entity_event_contextrenderer', 'render_group_id')

        # Adding field 'ContextRenderer.source_group'
        db.add_column(u'entity_event_contextrenderer', 'source_group',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entity_event.SourceGroup'], null=True),
                      keep_default=False)

        # Adding field 'ContextRenderer.rendering_style'
        db.add_column(u'entity_event_contextrenderer', 'rendering_style',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['entity_event.RenderingStyle']),
                      keep_default=False)


        # Changing field 'ContextRenderer.source'
        db.alter_column(u'entity_event_contextrenderer', 'source_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entity_event.Source'], null=True))
        # Adding unique constraint on 'ContextRenderer', fields ['source', 'rendering_style']
        db.create_unique(u'entity_event_contextrenderer', ['source_id', 'rendering_style_id'])

        # Deleting field 'Medium.render_group'
        db.delete_column(u'entity_event_medium', 'render_group_id')

        # Adding field 'Medium.rendering_style'
        db.add_column(u'entity_event_medium', 'rendering_style',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entity_event.RenderingStyle'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Removing unique constraint on 'ContextRenderer', fields ['source', 'rendering_style']
        db.delete_unique(u'entity_event_contextrenderer', ['source_id', 'rendering_style_id'])

        # Adding model 'RenderGroup'
        db.create_table(u'entity_event_rendergroup', (
            ('display_name', self.gf('django.db.models.fields.CharField')(default='', max_length=64)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, unique=True)),
        ))
        db.send_create_signal(u'entity_event', ['RenderGroup'])

        # Deleting model 'RenderingStyle'
        db.delete_table(u'entity_event_renderingstyle')

        # Adding field 'ContextRenderer.render_group'
        db.add_column(u'entity_event_contextrenderer', 'render_group',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['entity_event.RenderGroup']),
                      keep_default=False)

        # Deleting field 'ContextRenderer.source_group'
        db.delete_column(u'entity_event_contextrenderer', 'source_group_id')

        # Deleting field 'ContextRenderer.rendering_style'
        db.delete_column(u'entity_event_contextrenderer', 'rendering_style_id')


        # Changing field 'ContextRenderer.source'
        db.alter_column(u'entity_event_contextrenderer', 'source_id', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['entity_event.Source']))
        # Adding field 'Medium.render_group'
        db.add_column(u'entity_event_medium', 'render_group',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['entity_event.RenderGroup']),
                      keep_default=False)

        # Deleting field 'Medium.rendering_style'
        db.delete_column(u'entity_event_medium', 'rendering_style_id')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'entity.entity': {
            'Meta': {'unique_together': "(('entity_id', 'entity_type', 'entity_kind'),)", 'object_name': 'Entity'},
            'display_name': ('django.db.models.fields.TextField', [], {'db_index': 'True', 'blank': 'True'}),
            'entity_id': ('django.db.models.fields.IntegerField', [], {}),
            'entity_kind': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity.EntityKind']", 'on_delete': 'models.PROTECT'}),
            'entity_meta': ('jsonfield.fields.JSONField', [], {'null': 'True'}),
            'entity_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'on_delete': 'models.PROTECT'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'})
        },
        u'entity.entitykind': {
            'Meta': {'object_name': 'EntityKind'},
            'display_name': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256', 'db_index': 'True'})
        },
        u'entity_event.contextrenderer': {
            'Meta': {'unique_together': "(('source', 'rendering_style'),)", 'object_name': 'ContextRenderer'},
            'context_hints': ('jsonfield.fields.JSONField', [], {'default': 'None', 'null': 'True'}),
            'html_template': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'html_template_path': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'rendering_style': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_event.RenderingStyle']"}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_event.Source']", 'null': 'True'}),
            'source_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_event.SourceGroup']", 'null': 'True'}),
            'text_template': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'text_template_path': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'})
        },
        u'entity_event.event': {
            'Meta': {'object_name': 'Event'},
            'context': ('jsonfield.fields.JSONField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_event.Source']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'time_expires': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(9999, 12, 31, 0, 0)', 'db_index': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'entity_event.eventactor': {
            'Meta': {'object_name': 'EventActor'},
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity.Entity']"}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_event.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'entity_event.eventseen': {
            'Meta': {'unique_together': "(('event', 'medium'),)", 'object_name': 'EventSeen'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_event.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medium': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_event.Medium']"}),
            'time_seen': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'})
        },
        u'entity_event.medium': {
            'Meta': {'object_name': 'Medium'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'rendering_style': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_event.RenderingStyle']", 'null': 'True'})
        },
        u'entity_event.renderingstyle': {
            'Meta': {'object_name': 'RenderingStyle'},
            'display_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'entity_event.source': {
            'Meta': {'object_name': 'Source'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_event.SourceGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'entity_event.sourcegroup': {
            'Meta': {'object_name': 'SourceGroup'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'entity_event.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['entity.Entity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medium': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_event.Medium']"}),
            'only_following': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_event.Source']"}),
            'sub_entity_kind': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'+'", 'null': 'True', 'to': u"orm['entity.EntityKind']"})
        },
        u'entity_event.unsubscription': {
            'Meta': {'object_name': 'Unsubscription'},
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity.Entity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medium': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_event.Medium']"}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_event.Source']"})
        }
    }

    complete_apps = ['entity_event']