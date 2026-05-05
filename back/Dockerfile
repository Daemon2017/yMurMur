FROM ubuntu:18.04
WORKDIR /ymurmur
COPY install_deps.sh .
RUN sh install_deps.sh && rm install_deps.sh
COPY install_py.sh requirements.txt ./
RUN sh install_py.sh && rm install_py.sh
COPY install_compile.sh .
RUN sh install_compile.sh && rm install_compile.sh
COPY install_final.sh .
RUN sh install_final.sh && rm install_final.sh
COPY . .
CMD ["python3.8", "run.py"]
