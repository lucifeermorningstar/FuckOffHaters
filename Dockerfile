FROM sandy1709/catuserbot:alpine

#clonning repo 
RUN git clone https://github.com/lucifeermorningstar/FuckOffHaters.git /root/DaisyX
#working directory
WORKDIR /root/DaisyX

# Install requirements
RUN sudo pip3 install -U -r requirements.txt

ENV PATH="/home/DaisyX/bin:$PATH"

# Starting Worker
CMD ["python3","-m","DaisyX"]
