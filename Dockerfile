FROM python:3.10.8-alpine3.16
WORKDIR /bot
ENV TZ=Europe/Madrid

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY . .

# Run the bot
CMD ["python", "-u", "bot.py"]