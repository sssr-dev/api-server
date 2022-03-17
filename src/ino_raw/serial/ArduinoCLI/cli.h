class ArduinoCLI {

    private:
    char* PROMPT_IN = ":> ";
    char* PROMPT_OUT = "]: ";
    String cmd;

    void print_hello_message(){

        println("Script made by SantaSpeen.");
        println("Hello world!");
        println("Type 'help' for more information.");
        print(PROMPT_IN);

    }

    public:
    void start(){
        while (1){

            if (Serial.available() > 0) {

                cmd = input();
                println(cmd);
                print(PROMPT_OUT);
                println(cmd);
                print(PROMPT_IN);

            }

        }
    }
};