# radiotherapy-qc-image-analysis
Automated image analysis for radiotherapy quality control using Python and OpenCV

# Análisis Automatizado de Placas Radiológicas para Control de Calidad

## Descripción
Proyecto enfocado en el desarrollo de una herramienta automatizada para el control de calidad del haz de radiación en un acelerador lineal, a partir del análisis de placas radiológicas. El objetivo es evaluar de manera objetiva la coincidencia entre el campo luminoso visible y el haz real de radiación, un criterio crítico en radioterapia.

## Objetivo
Diseñar e implementar un método reproducible y basado en métricas físicas que permita cuantificar desviaciones geométricas entre el campo luminoso y el haz de radiación, reduciendo la dependencia de evaluaciones subjetivas y asegurando el cumplimiento de tolerancias de calidad.

## Datos
El proyecto trabaja con imágenes radiológicas obtenidas en pruebas de control de calidad en un entorno clínico.  
Por motivos de confidencialidad, los datos reales no se incluyen en este repositorio.

Las imágenes corresponden a datos no estructurados con variaciones de intensidad, ruido y zonas de transición relevantes para el análisis geométrico del campo de radiación.

## Metodología
El enfoque se basa en técnicas de procesamiento de imágenes utilizando Python y OpenCV.  
Se aplican etapas de preprocesamiento para mejorar la calidad de la información, seguidas de la detección de zonas de transición de intensidad asociadas a los bordes del campo luminoso y del haz de radiación.

Las desviaciones geométricas se calculan y expresan en unidades físicas relevantes para protocolos de control de calidad.  
La validación del método se realiza mediante análisis estadístico descriptivo, contrastando los resultados con tolerancias aceptadas en control de calidad radioterapéutico.

Se priorizan soluciones interpretables, simples y reproducibles sobre enfoques excesivamente complejos que dificulten la trazabilidad y validación física de los resultados.

## Resultados
La herramienta permite automatizar la evaluación de la coincidencia entre el campo luminoso y el haz de radiación, identificando de forma consistente las zonas de transición de intensidad y cuantificando desviaciones geométricas.

El principal aporte del proyecto es la estandarización del proceso de control de calidad, garantizando resultados reproducibles y comparables frente a criterios objetivos.

## Tecnologías
- Python
- OpenCV
- Procesamiento de imágenes
- Análisis estadístico descriptivo

## Reproducibilidad
Para ejecutar el análisis:
1. Clonar el repositorio.
2. Crear un entorno virtual.
3. Instalar las dependencias desde `requirements.txt`.
4. Ejecutar el notebook ubicado en la carpeta `notebooks/`.

Este repositorio no incluye datos clínicos reales. En su lugar, se describe el flujo de trabajo y las decisiones técnicas del análisis.
