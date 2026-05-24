FROM n8nio/runners:latest

USER root
RUN mkdir -p /home/runner/.n8n/python_modules && chown -R runner:runner /home/runner/.n8n
# Установка pip в виртуальном окружении
RUN /opt/runners/task-runner-python/.venv/bin/python -m ensurepip --upgrade
# Установка lxml вместе с вашими пакетами
RUN /opt/runners/task-runner-python/.venv/bin/python -m pip install requests beautifulsoup4 lxml

USER runner