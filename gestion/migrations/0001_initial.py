# Generated by Django 4.2.5 on 2023-11-01 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(default='Comisión nueva')),
                ('resolucion', models.FileField(blank=True, null=True, upload_to='uploads/')),
                ('departamento', models.CharField(choices=[('Informatica', 'Informatica'), ('Minas', 'Minas'), ('Electronica', 'Electronica'), ('Agrimensura', 'Agrimensura')], default='Informatica')),
            ],
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('descripcion', models.TextField()),
                ('fecha_presentacion', models.DateField(blank=True)),
                ('proyecto_escrito', models.FileField(upload_to='uploads/')),
                ('certificado_analitico', models.FileField(upload_to='uploads/')),
                ('nota_aceptacion', models.FileField(upload_to='uploads/')),
            ],
        ),
        migrations.CreateModel(
            name='Tribunal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disposicion', models.FileField(upload_to='uploads/')),
                ('fecha_disposicion', models.DateField()),
                ('numero_disposicion', models.CharField(max_length=50)),
                ('proyecto', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='tribunal_proyecto', to='gestion.proyecto')),
            ],
        ),
        migrations.CreateModel(
            name='TrabajoFinal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrador', models.FileField(upload_to='uploads/')),
                ('aceptacion_director', models.FileField(upload_to='uploads/')),
                ('fecha_presentacion', models.DateField()),
                ('proyecto', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='tf_proyecto', to='gestion.proyecto')),
            ],
        ),
        migrations.CreateModel(
            name='InstanciaEvaluacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(choices=[('COMISION DE SEGUIMIENTO', 'COMISION DE SEGUIMIENTO'), ('TRIBUNAL EVALUADOR', 'TRIBUNAL EVALUADOR'), ('TRABAJO FINAL BORRADOR', 'TRABAJO FINAL BORRADOR'), ('DEFENSA TRABAJO FINAL', 'DEFENSA TRABAJO FINAL'), ('FINALIZADO', 'FINALIZADO')])),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proyecto_instancia', to='gestion.proyecto')),
            ],
        ),
        migrations.CreateModel(
            name='Evaluacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('informe', models.FileField(upload_to='uploads/')),
                ('fecha', models.DateField()),
                ('estado', models.CharField(choices=[('OBSERVADO', 'OBSERVADO'), ('APROBADO', 'APROBADO'), ('RECHAZADO', 'RECHAZADO')])),
                ('observacion', models.TextField()),
                ('nuevoPTF', models.FileField(blank=True, null=True, upload_to='uploads/')),
                ('instancia_evaluacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instancia_evaluacion', to='gestion.instanciaevaluacion')),
            ],
        ),
        migrations.CreateModel(
            name='Defensa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('nota', models.IntegerField(blank=True, null=True)),
                ('acta', models.FileField(blank=True, null=True, upload_to='uploads/')),
                ('proyecto', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='defensa_proyecto', to='gestion.proyecto')),
            ],
        ),
        migrations.CreateModel(
            name='ComisionProyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_alta', models.DateField()),
                ('comision', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='proyecto_comision', to='gestion.comision')),
                ('proyecto', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='comision_proyecto', to='gestion.proyecto')),
            ],
        ),
    ]
