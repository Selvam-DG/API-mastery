#  API Mastery in Python

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

A comprehensive collection of hands-on API projects built using Python. This repository serves as both a learning resource and a practical reference for implementing various API architectures and communication protocols.

---

## Table of Contents

- [What is an API?](#what-is-an-api)
- [Why Use APIs?](#why-use-apis)
- [Advantages of APIs](#advantages-of-apis)
- [Challenges and Considerations](#challenges-and-considerations)
- [Types of APIs](#types-of-apis)
- [Projects in This Repository](#projects-in-this-repository)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [License](#license)

---

##  What is an API?

**API (Application Programming Interface)** is a set of rules, protocols, and tools that allows different software applications to communicate with each other. Think of it as a waiter in a restaurant: you (the client) tell the waiter (API) what you want, the waiter communicates your order to the kitchen (server), and then brings back your food (response).

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Client    │ Request │     API     │ Request │   Server    │
│ Application │────────▶│  Interface  │────────▶│  Database   │
│             │◀────────│             │◀────────│             │
└─────────────┘ Response└─────────────┘ Response└─────────────┘
```

### Key Components:

- **Endpoint**: A specific URL where an API can be accessed
- **Request**: What the client sends to the API (method, headers, body)
- **Response**: What the API sends back (status code, data)
- **Authentication**: Mechanism to verify who is making the request
- **Rate Limiting**: Controls on how many requests can be made

---

##  Why Use APIs?

APIs have become the backbone of modern software development for several compelling reasons:

### 1. **Modularity & Separation of Concerns**
APIs allow you to separate your application into independent services. Frontend developers can work independently from backend developers, as long as they agree on the API contract.

### 2. **Reusability**
Write once, use everywhere. A well-designed API can serve multiple client applications (web, mobile, IoT) simultaneously.

### 3. **Scalability**
APIs enable horizontal scaling. You can scale different parts of your application independently based on demand.

### 4. **Integration & Ecosystem**
APIs allow different systems to work together. They enable you to leverage third-party services (payment gateways, authentication, maps, etc.) without building everything from scratch.

### 5. **Security**
APIs provide a controlled way to expose functionality. You can implement authentication, authorization, and rate limiting to protect your resources.

### 6. **Innovation**
APIs enable developers to build on top of existing platforms, fostering innovation and creating new use cases the original creators never imagined.

---

## Advantages of APIs

| Advantage | Description | Example |
|-----------|-------------|---------|
| **Abstraction** | Hide complex implementation details | Payment APIs hide complex banking integrations |
| **Interoperability** | Different systems can communicate | Mobile app talking to a web server |
| **Automation** | Enable machine-to-machine communication | CI/CD pipelines using GitHub API |
| **Efficiency** | Reduce development time and costs | Using Google Maps API instead of building your own |
| **Real-time Updates** | Push or pull data as it changes | WebSocket APIs for live sports scores |
| **Platform Independence** | Work across different technologies | Java client consuming a Python API |
| **Version Control** | Maintain multiple API versions | `/api/v1/` and `/api/v2/` endpoints |
| **Monetization** | Create new revenue streams | Stripe API charges per transaction |

---

## Challenges and Considerations

### Disadvantages:

1. **Complexity**: Designing a good API requires careful planning and expertise
2. **Breaking Changes**: Modifying APIs can break existing client applications
3. **Security Risks**: APIs are attack vectors if not properly secured
4. **Performance Overhead**: Network latency and serialization can impact speed
5. **Dependency Management**: You're dependent on third-party API availability
6. **Documentation Maintenance**: APIs require comprehensive, up-to-date documentation
7. **Rate Limiting Issues**: Third-party APIs may have usage limits
8. **Versioning Challenges**: Supporting multiple versions increases maintenance burden

### Best Practices to Mitigate Issues:

- Implement proper authentication and authorization (OAuth 2.0, JWT)
- Use HTTPS for all API communications
- Version your APIs from the start
- Provide comprehensive documentation (OpenAPI/Swagger)
- Implement rate limiting and throttling
- Monitor API usage and performance
- Use caching strategies where appropriate
- Design for backward compatibility

---

## Types of APIs

### 1. REST (Representational State Transfer)

**REST** is an architectural style that uses standard HTTP methods and is stateless by design.

#### Characteristics:
- Uses HTTP methods: GET, POST, PUT, DELETE, PATCH
- Stateless communication
- Resource-based URLs
- JSON or XML data format
- Cacheable responses

#### Use Cases:
- Public APIs (Twitter, GitHub, Stripe)
- Mobile applications
- Web services
- Microservices architecture

#### Real-World Examples:
- **Twitter API**: Tweet creation, user data retrieval
- **GitHub API**: Repository management, issue tracking
- **Stripe API**: Payment processing
- **OpenWeatherMap**: Weather data retrieval

#### Request Example:
```http
GET /api/users/123 HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### Response Example:
```json
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2025-01-15T10:30:00Z"
}
```

**Project:** [rest-task-manager/](./rest-task-manager/)

---

### 2. WebSocket

**WebSocket** provides full-duplex, bidirectional communication channels over a single TCP connection.

#### Characteristics:
- Persistent connection
- Real-time, bidirectional communication
- Low latency
- Event-driven architecture
- Efficient for frequent updates

#### Use Cases:
- Real-time chat applications
- Live notifications
- Collaborative editing tools
- Live sports scores
- Stock market tickers
- Multiplayer gaming

#### Real-World Examples:
- **Slack**: Real-time messaging
- **Discord**: Voice and text chat
- **Trello**: Live board updates
- **Trading platforms**: Real-time stock prices
- **Google Docs**: Collaborative editing

#### Connection Flow:
```
Client                          Server
  |                               |
  |------- HTTP Upgrade --------->|
  |                               |
  |<----- 101 Switching Protocols-|
  |                               |
  |<======== WebSocket ==========>|
  |         (Bidirectional)       |
```

**Project:** [websocket-chat-app/](./websocket-chat-app/)

---

### 3. GraphQL

**GraphQL** is a query language for APIs that allows clients to request exactly the data they need.

#### Characteristics:
- Single endpoint
- Client-specified queries
- Strongly typed schema
- No over-fetching or under-fetching
- Real-time updates with subscriptions

#### Use Cases:
- Complex data requirements
- Mobile applications (reduce bandwidth)
- Rapid frontend development
- Aggregating multiple data sources

#### Real-World Examples:
- **GitHub**: Complex repository queries
- **Shopify**: E-commerce product data
- **Facebook**: News feed and social data
- **Twitter**: Tweet and user data
- **Yelp**: Business and review data

#### Query Example:
```graphql
query {
  user(id: "123") {
    name
    email
    posts(limit: 5) {
      title
      createdAt
      comments {
        text
        author
      }
    }
  }
}
```

#### Advantages over REST:
- Fetch multiple resources in a single request
- No versioning needed
- Strong typing and introspection
- Excellent developer experience

**Project:** [graphql-blog-api/](./graphql-blog-api/)

---

### 4. SOAP (Simple Object Access Protocol)

**SOAP** is a protocol for exchanging structured information using XML.

#### Characteristics:
- XML-based messaging
- Strict standards and contracts (WSDL)
- Built-in error handling
- Platform and language independent
- WS-Security for security

#### Use Cases:
- Enterprise applications
- Financial transactions
- Telecommunication services
- Legacy system integration
- High-security requirements

#### Real-World Examples:
- **PayPal**: Payment gateway (also offers REST)
- **Salesforce**: CRM operations
- **Banking systems**: Financial transactions
- **Government services**: Tax filing, permits
- **Healthcare**: Patient record systems (HL7)

#### Request Example:
```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetStudent xmlns="http://example.com/students">
      <StudentId>12345</StudentId>
    </GetStudent>
  </soap:Body>
</soap:Envelope>
```

**Project:** [soap-student-service/](./soap-student-service/)

---

### 5. WebRTC (Web Real-Time Communication)

**WebRTC** enables real-time peer-to-peer communication of audio, video, and data.

#### Characteristics:
- Peer-to-peer communication
- Low latency
- Built-in encryption (DTLS/SRTP)
- NAT traversal
- Browser-native support

#### Use Cases:
- Video conferencing
- Voice calling
- Screen sharing
- File transfer
- Live streaming
- Remote desktop applications

#### Real-World Examples:
- **Zoom**: Video conferencing
- **Google Meet**: Video meetings
- **Discord**: Voice and video chat
- **WhatsApp Web**: Voice/video calls
- **Twitch**: Live streaming
- **Facebook Messenger**: Video calls

#### Connection Flow:
```
Peer A                 Signaling Server              Peer B
  |                            |                        |
  |-------- Offer ------------>|                        |
  |                            |-------- Offer -------->|
  |                            |                        |
  |                            |<------ Answer ---------|
  |<------ Answer -------------|                        |
  |                            |                        |
  |<============== Direct P2P Connection =============>|
```

**Project:** [webrtc-video-call/](./webrtc-video-call/)

---

### 6. Push Notifications

**Push Notifications** send real-time messages from server to client without client polling.

#### Characteristics:
- Server-initiated communication
- Persistent connection or device tokens
- Platform-specific protocols (APNs, FCM)
- Background delivery
- User engagement tool

#### Use Cases:
- Mobile app notifications
- Breaking news alerts
- E-commerce updates
- Social media notifications
- System alerts and monitoring

#### Real-World Examples:
- **WhatsApp**: Message notifications
- **Instagram**: Like and comment alerts
- **Amazon**: Order status updates
- **News apps**: Breaking news alerts
- **Banking apps**: Transaction alerts
- **Uber**: Ride status updates

#### Technologies:
- **FCM** (Firebase Cloud Messaging): Android & iOS
- **APNs** (Apple Push Notification Service): iOS
- **Web Push**: Browser notifications
- **OneSignal**: Cross-platform push service

**Project:** [push-server/](./push-server/)

---

### 7. Webhooks 

**Webhooks** are user-defined HTTP callbacks triggered by specific events.

#### Characteristics:
- Event-driven
- Server-to-server communication
- Push-based (no polling)
- Asynchronous
- Payload delivery on events

#### Use Cases:
- Payment confirmations
- CI/CD pipelines
- CRM integrations
- Automated workflows
- Monitoring and alerting

#### Real-World Examples:
- **Stripe**: Payment success/failure events
- **GitHub**: Repository push, PR events
- **Shopify**: Order creation, product updates
- **Mailchimp**: Email campaign events
- **Twilio**: SMS delivery status
- **Slack**: App integrations and bots

#### Workflow:
```
┌─────────┐        Event        ┌──────────┐
│ Service │      Occurs         │  Your    │
│ Provider│──────────┬─────────▶│  Server  │
│ (GitHub)│          │          │          │
└─────────┘          │          └──────────┘
                     │
              POST /webhook
              {
                "event": "push",
                "repository": "...",
                "commits": [...]
              }
```

**Project:** [webhook-listener/](./webhook-listener/)

---

## Projects in This Repository

Each project is a fully functional implementation with its own README, setup instructions, and examples.

| Project | API Type | Description | Key Technologies |
|---------|----------|-------------|------------------|
| [REST Task Manager](./rest-task-manager/) | REST | Full-featured task management API with CRUD operations | Flask, SQLAlchemy, JWT |
| [WebSocket Chat App](./websocket-chat-app/) | WebSocket | Real-time chat application with multiple rooms | Socket.io, Redis |
| [GraphQL Blog API](./graphql-blog-api/) | GraphQL | Blog platform with posts, comments, and users | Graphene, Django |
| [SOAP Student Service](./soap-student-service/) | SOAP | Student management system with WSDL | Zeep, lxml |
| [Push Notification Server](./push-server/) | Push | Multi-platform push notification service | Firebase, APNs |
| [Webhook Listener](./webhook-listener/) | Webhook | Receive and process webhook events | FastAPI, Celery |
| [WebRTC Video Call](./webrtc-video-call/) | WebRTC | Peer-to-peer video calling application | aiortc, WebSockets |

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/Selvam-DG/api-mastery.git
   cd api-mastery
   ```

2. **Choose a project**
   ```bash
   cd rest-task-manager  # or any other project
   ```

3. **Follow the project-specific README**
   Each project contains detailed setup and usage instructions.

### General Setup Pattern

Most projects follow this structure:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py  # or main.py, depending on the project
```

---

## API Comparison Chart

| Feature | REST | WebSocket | GraphQL | SOAP | WebRTC | Webhooks |
|---------|------|-----------|---------|------|--------|----------|
| **Communication** | Request-Response | Bidirectional | Request-Response | Request-Response | P2P | Event-Driven |
| **Protocol** | HTTP/HTTPS | WS/WSS | HTTP/HTTPS | HTTP/HTTPS/SMTP | UDP/TCP | HTTP/HTTPS |
| **Data Format** | JSON/XML | Text/Binary | JSON | XML | Binary | JSON/XML |
| **Real-time** | ❌ | ✅ | Partial | ❌ | ✅ | ✅ |
| **Complexity** | Low | Medium | Medium | High | High | Low |
| **Stateful** | ❌ | ✅ | ❌ | Can be | ✅ | ❌ |
| **Bandwidth** | Medium | Low | Low | High | High | Low |
| **Learning Curve** | Easy | Medium | Medium | Steep | Steep | Easy |
| **Caching** | ✅ | ❌ | Complex | ❌ | ❌ | ❌ |

---

## When to Use Which API?

### Use REST when:
- Building standard CRUD applications
- You need caching capabilities
- Stateless operations are sufficient
- You want broad compatibility

### Use WebSocket when:
- Real-time bidirectional communication is needed
- Building chat applications, live updates
- You need low latency
- Persistent connection is beneficial

### Use GraphQL when:
- Clients have varying data requirements
- You want to minimize over-fetching
- Building mobile apps with bandwidth constraints
- You need a flexible, evolvable API

### Use SOAP when:
- Working with enterprise systems
- Strict contracts are required (WSDL)
- You need built-in security standards
- Working with legacy systems

### Use WebRTC when:
- Building video/audio communication apps
- Peer-to-peer data transfer is needed
- Low latency is critical
- You need encrypted media streams

### Use Webhooks when:
- You need event-driven architecture
- Avoiding constant polling
- Integrating with third-party services
- Building automation workflows

---

## Development Tools & Resources

### API Testing Tools:
- **Postman**: REST, GraphQL, WebSocket testing
- **Insomnia**: REST and GraphQL client
- **cURL**: Command-line HTTP client
- **SoapUI**: SOAP and REST testing
- **websocat**: WebSocket command-line client

### Documentation Tools:
- **Swagger/OpenAPI**: REST API documentation
- **GraphQL Playground**: GraphQL IDE
- **Redoc**: OpenAPI documentation generator
- **Postman Collections**: Shareable API collections

### Monitoring & Analytics:
- **Prometheus**: Metrics collection
- **Grafana**: Metrics visualization
- **ELK Stack**: Log management
- **New Relic**: Application monitoring

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your code follows PEP 8 style guidelines and includes appropriate tests.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contact & Support

- **Issues**: [GitHub Issues](https://github.com/Selvam-DG/api-mastery/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Selvam-DG/api-mastery/discussions)
- **Email**: dasariselvam321@gmail.com

---

## Acknowledgments

- Python Software Foundation
- All the amazing open-source libraries used in these projects
- The developer community for inspiration and support

---

## Additional Resources

### Books:
- "RESTful Web APIs" by Leonard Richardson & Mike Amundsen
- "Designing Data-Intensive Applications" by Martin Kleppmann
- "GraphQL in Action" by Samer Buna

### Online Courses:
- [REST API Design, Development & Management (Udemy)](https://www.udemy.com/course/rest-api/)
- [GraphQL: The Complete Guide (Udemy)](https://www.udemy.com/course/graphql-bootcamp/)
- [WebSocket Programming (Pluralsight)](https://www.pluralsight.com/)

### Official Documentation:
- [REST API Tutorial](https://restfulapi.net/)
- [GraphQL Documentation](https://graphql.org/learn/)
- [WebSocket API (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [WebRTC Documentation](https://webrtc.org/)

---

<div align="center">

### ⭐ Star this repository if you find it helpful!

**Happy Coding! 🚀**

Made with ❤️ by developers, for developers

</div>