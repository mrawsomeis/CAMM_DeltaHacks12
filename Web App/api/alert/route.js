// Store for connected clients
let clients = [];

// Handle OPTIONS preflight request
export async function OPTIONS(req) {
  return new Response(null, {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      'Access-Control-Allow-Credentials': 'true',
    },
  });
}

export async function GET(req) {
  const headers = {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Credentials': 'true',
  };

  const stream = new ReadableStream({
    start(controller) {
      const clientId = Date.now();
      const encoder = new TextEncoder();
      
      const client = {
        id: clientId,
        controller,
        send: (data) => {
          try {
            controller.enqueue(encoder.encode(`data: ${JSON.stringify(data)}\n\n`));
          } catch (error) {
            console.error('Error sending data:', error);
          }
        }
      };
      
      clients.push(client);
      console.log(`Client ${clientId} connected. Total: ${clients.length}`);

      // Send connection confirmation
      client.send({ type: 'CONNECTED', message: 'Monitoring for fall detection' });

      // Keep-alive
      const keepAlive = setInterval(() => {
        try {
          controller.enqueue(encoder.encode(': keepalive\n\n'));
        } catch (error) {
          clearInterval(keepAlive);
        }
      }, 30000);

      // Cleanup on disconnect
      req.signal.addEventListener('abort', () => {
        console.log(`Client ${clientId} disconnected`);
        clearInterval(keepAlive);
        clients = clients.filter(c => c.id !== clientId);
        try {
          controller.close();
        } catch (error) {
          // Already closed
        }
      });
    },
  });

  return new Response(stream, { headers });
}

export async function POST(req) {
  try {
    const { userId, address, fallDetected } = await req.json();

    if (!fallDetected) {
      return new Response(
        JSON.stringify({ success: false, error: 'No fall detected' }),
        { 
          status: 400,
          headers: { 
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
          }
        }
      );
    }

    console.log(`🚨 Fall detected! User: ${userId}, Location: ${address}`);

    const alertMessage = `Emergency: Person has fallen and is unresponsive at ${address}. ${
      userId ? `User ID: ${userId}.` : ''
    } Immediate assistance required. Call 911 if you are nearby.`;

    const eventData = {
      type: 'FALL_DETECTED',
      timestamp: new Date().toISOString(),
      userId: userId || 'Unknown',
      address: address || 'Unknown location',
      message: alertMessage,
    };

    console.log(`Broadcasting to ${clients.length} clients`);

    clients.forEach((client) => {
      try {
        client.send(eventData);
      } catch (error) {
        console.error(`Failed to send to client ${client.id}:`, error);
      }
    });

    return new Response(
      JSON.stringify({ 
        success: true, 
        clientsNotified: clients.length,
        eventData 
      }),
      {
        status: 200,
        headers: { 
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
      }
    );
  } catch (error) {
    console.error('Error handling fall detection:', error);
    return new Response(
      JSON.stringify({ success: false, error: error.message }),
      { 
        status: 500,
        headers: { 
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        }
      }
    );
  }
}
