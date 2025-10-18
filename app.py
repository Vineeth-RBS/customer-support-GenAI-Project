from flask import Flask, jsonify
from dotenv import load_dotenv
import os
from models import Base, get_engine_and_session, Order,Customer,Ticket


load_dotenv()
app = Flask(__name__)

# ---- Database setup ---- #
engine, Session = get_engine_and_session()
Base.metadata.create_all(bind=engine)   # Create tables if not exist

@app.route("/order/<int:order_id>", methods = ['GET'])
def getOrderDetails(order_id):
    session = Session()
    order = session.query(Order).filter(Order.id==order_id).first()
    if not order:
        return jsonify({"error":"No Order Found"}),404
    
    order_data = {
        "order_id":order.id,
        "product_name":order.product_name,
        "order_status":order.order_status,
        "expected_delivery":str(order.expected_delivery),
        "last_updated": str(order.last_updated),
        "customer": {
            "id": order.customer.id,
            "name": order.customer.name,
            "email": order.customer.email,
            "phone": order.customer.phone
        },
        "tickets":[{
            "ticket_id":t.id,
            "issue": t.issue,
            "status": t.status,
            "created_at": str(t.created_at),
            "updated_at": str(t.updated_at)
        
        }for t in order.tickets
        ]
    }
    session.close()
    return jsonify(order_data)
    

if __name__ == "__main__":
    app.run(debug=True, port=5000)
