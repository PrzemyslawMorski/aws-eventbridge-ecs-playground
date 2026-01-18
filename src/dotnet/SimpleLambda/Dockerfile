# Build stage
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src

# Copy csproj and restore dependencies
COPY SimpleLambda.csproj .
RUN dotnet restore

# Copy everything else and build
COPY . .
RUN dotnet publish -c Release -o /app/publish

# Runtime stage
FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS runtime
WORKDIR /var/task

# Install Lambda Runtime Interface Client
RUN apt-get update && \
    apt-get install -y \
    g++ \
    make \
    unzip \
    libunwind-dev \
    curl && \
    curl -sSL https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie -o /usr/local/bin/aws-lambda-rie && \
    chmod +x /usr/local/bin/aws-lambda-rie && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy published app
COPY --from=build /app/publish .

# Set the handler
ENTRYPOINT ["/usr/local/bin/aws-lambda-rie", "dotnet", "SimpleLambda.dll"]
