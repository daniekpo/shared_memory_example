from environment import MyAppEnvironment

if __name__ == "__main__":
    print("Started")
    with MyAppEnvironment() as env:
        for _ in range(1000):
            result = env.tick()
            print("Value in shared memory: %d" %(result))
    
    print("Done")