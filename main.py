from agent import UdaPlayAgent

agent = UdaPlayAgent()

print("🎮 UdaPlay AI Ready (type 'exit' to quit)\n")

while True:
    q = input("Ask: ")
    if q.lower() == "exit":
        break

    print(agent.answer(q))