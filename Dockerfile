FROM python:3.11.1-slim-bullseye
WORKDIR /bot
ENV TZ=Europe/Madrid

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY . .

# Run the bot
CMD ["python", "-u", "bot.py"]