using System.Text.Json;
using Amazon.Lambda.Core;
using Amazon.Lambda.RuntimeSupport;
using Amazon.Lambda.Serialization.SystemTextJson;

namespace SimpleLambda;

public class Function
{
    private static async Task Main()
    {
        var handler = FunctionHandler;
        await LambdaBootstrapBuilder.Create(handler, new LambdaJsonSerializer())
            .Build()
            .RunAsync();
    }

    public static async Task<string> FunctionHandler(object input, ILambdaContext context)
    {
        context.Logger.LogInformation($"Received input: {JsonSerializer.Serialize(input)}");
        
        var response = new
        {
            Message = "Hello from .NET Lambda running in LocalStack!",
            Timestamp = DateTime.UtcNow,
            Input = input
        };

        context.Logger.LogInformation($"Returning response: {JsonSerializer.Serialize(response)}");
        
        return JsonSerializer.Serialize(response);
    }
}
