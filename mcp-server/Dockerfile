# Multi-stage build for Spring Boot application
FROM eclipse-temurin:17-jdk as builder

WORKDIR /app

# Copy gradle files
COPY gradlew .
COPY gradle gradle
COPY build.gradle .
COPY settings.gradle .

# Copy source code
COPY src src

# Build the application
RUN chmod +x gradlew
RUN ./gradlew clean build -x test

# Runtime stage
FROM eclipse-temurin:17-jre

WORKDIR /app

# Copy the built jar
COPY --from=builder /app/build/libs/*.jar app.jar

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/mcp/health || exit 1

# Run the application
ENTRYPOINT ["java", "-jar", "app.jar"]
