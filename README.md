# Pesiton RAG System 

## Setup Instructions

1. Clone the repository and add the following environment variables to a `.env` file to the `api` folder

```env 
BEDROCK_KEY=***************
MONGODB_URL=***************
COLLECTION_NAME=products
```

2. Navigate to the root directory and run the following docker command to build and start the container. 

```bash 
docker build -t pesiton-rag-system:v1 .
docker run -d -p 8000:8000  pesiton-rag-system:v1
```

## Endpoints 

Request Example:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/query' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "What about wireless ones?",
  "type":"product",
  "top_k": 5,
  "chat_history": [
    {
      "role": "user",
      "content": "headphones with active noise cancellation for under $100"
    },
    {
      "role": "assistant",
      "content": "I couldnt find any headphones with active noise cancellation"
    }
  ]
}'
```

Response Example: 

```json 
{
  "query": "What about wireless ones?",
  "type": "product",
  "answer": "The provided context does not include any wireless headphones with active noise cancellation under $100.",
  "sources": [
    {
      "content": "New Mini White Noise Machine 22 Soothing Sounds ABS Material Babies Kids Adults-Portable Home Use 900mAh Battery 20+ Hours",
      "metadata": {
        "document_id": "6928830d40737c4e81cacfbe",
        "productName": "New Mini White Noise Machine 22 Soothing Sounds ABS Material Babies Kids Adults-Portable Home Use 900mAh Battery 20+ Hours",
        "modelNumber": "MODEL-NEW-MINI-WHITE-NOISE"
      },
      "score": 0.5948014855384827
    },
    {
      "content": "2026 New Multi-color White Noise Machine Night Light Timer 22 Soothing Sounds Battery Powered 100 Hours Playtime for Adults Kids",
      "metadata": {
        "document_id": "6928830e40737c4e81cacfc0",
        "productName": "2026 New Multi-color White Noise Machine Night Light Timer 22 Soothing Sounds Battery Powered 100 Hours Playtime for Adults Kids",
        "modelNumber": "MODEL-2026-NEW-MULTI-COLOR"
      },
      "score": 0.593498170375824
    },
    {
      "content": "2025 Hot Selling 4-in-1 Foldable Car Charger Adapter LED Display 120W Fast Charging Type C Retractable Cable PD Car Phone",
      "metadata": {
        "document_id": "6928831240737c4e81cacfe5",
        "productName": "2025 Hot Selling 4-in-1 Foldable Car Charger Adapter LED Display 120W Fast Charging Type C Retractable Cable PD Car Phone",
        "modelNumber": "MODEL-2025-HOT-SELLING-4-I"
      },
      "score": 0.5919401049613953
    },
    {
      "content": "140W Mag 3 to USB-C Braided Cable with 180 Degree Rotating Head Magnetic Interface 2M Cable for Mac Book",
      "metadata": {
        "document_id": "6928831040737c4e81cacfd5",
        "productName": "140W Mag 3 to USB-C Braided Cable with 180 Degree Rotating Head Magnetic Interface 2M Cable for Mac Book",
        "modelNumber": "MODEL-140W-MAG-3-TO-USB-C-"
      },
      "score": 0.5892583727836609
    },
    {
      "content": "New Design 4-in-1 Foldable 120W Fast Charging Type C Car Charger Adapter LED Display QC3.0 Retractable Cable for PD Car Phone",
      "metadata": {
        "document_id": "6928831140737c4e81cacfe3",
        "productName": "New Design 4-in-1 Foldable 120W Fast Charging Type C Car Charger Adapter LED Display QC3.0 Retractable Cable for PD Car Phone",
        "modelNumber": "MODEL-NEW-DESIGN-4-IN-1-FO"
      },
      "score": 0.5885190367698669
    }
  ]
}
```

You can use the score values to order the source documents based on their relevance to the query , with higher scores indicating greater relevance.