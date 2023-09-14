#include <iostream>
#include <vector>
#include <time.h>
#include <fstream>
#include <sstream>
#include <SFML/Graphics.hpp>
#include <SFML/System.hpp>
#include <nlohmann/json.hpp>

int main() {
    srand(time(NULL)); //needed for generating "stars" in background - they are generated in the random places

    std::ifstream file("10k80ms2s-trimed.json");
    if (!file.is_open()) {
        std::cerr << "Failed to open .json file" << std::endl;
        return 1;
    }//opening file with needed data / error message if file not loaded

    nlohmann::json examplesData;
    file >> examplesData;//writing data into variable


    sf::Font font;
    if (!font.loadFromFile("arial.ttf")) {
        return EXIT_FAILURE;
    }//loading font for displaying texts

    sf::RenderWindow window(sf::VideoMode(800, 800), "Graphic Representation of Problems");

    int totalIterations = examplesData["iterations_amount"];
    int currentIteration = 0;

    const int nStars = 100;
    std::vector<sf::CircleShape> stars(nStars);
    for (int i = 0; i < nStars; i++) {
        sf::CircleShape star(1);
        star.setFillColor(sf::Color::White);
        star.setPosition(rand() % 800, rand() % 800);
        stars[i] = star;
    }//all of this sequence creates tiny spots in the background - "stars"

    while (currentIteration < totalIterations) {
        const auto& example = examplesData["iterations"][currentIteration];
        int amount = example["amount"];
        int frames = example["frames"];
      
        std::vector<sf::CircleShape> planets_model(amount);
        std::vector<float> mass; //same for model planets and given ones
        std::vector<std::vector<sf::Vector2f>> positions_model; //positions of model planets
        
        const auto& examples_2 = examplesData["iterations"][currentIteration + 1];
        std::vector<sf::CircleShape> planets_true(amount);
        std::vector<std::vector<sf::Vector2f>> positions_true;//inforamtion about the right positions of planets


        for (const auto& planetData : example["planets"]) {
            float mass_tmp = planetData["mass"];
            mass.push_back(mass_tmp);

            std::vector<sf::Vector2f> positions_model_tmp;
            for (const auto& positionData : planetData["positions"]) {
                float x = positionData["x"];
                float y = positionData["y"];
                positions_model_tmp.emplace_back(x, y);
            }
            positions_model.push_back(positions_model_tmp);
        }//we write the positions for each planet here

        for (const auto& planetData_true : examples_2["planets"]) {
            std::vector<sf::Vector2f> positions_true_tmp;
            for (const auto& positionData : planetData_true["positions"]) {
                float x = positionData["x"];
                float y = positionData["y"];
                positions_true_tmp.emplace_back(x, y);
            }
            positions_true.push_back(positions_true_tmp);
        }//we write the right position for every planet


        sf::Clock clock;
        float updateTime = example["delta"];
        float elapsedTime = 0.0f;
        int currentFrame = 0;//the part where all of needed parameters for animation are defined

        bool nextIteration = false;
        bool previousIteration = false;//parameters needed for navigating between iterations

        while (window.isOpen()) {
            sf::Event event;
            while (window.pollEvent(event)) {
                if (event.type == sf::Event::Closed) {
                    window.close();
                }
                if (event.type == sf::Event::KeyPressed) {
                    if (event.key.code == sf::Keyboard::Right) {
                        nextIteration = true; //right arrow pressed -> next iteration
                    }
                    else if (event.key.code == sf::Keyboard::Left) {
                        previousIteration = true; //left arrow pressed -> previous iteration
                    }
                }
            }
            window.clear();

            for (const auto& star : stars) {

                window.draw(star);//drawings stars

            }

            for (int i = 0; i < amount; i++) {
                float radius = 25.0f * mass[i]; //setting radius linked to mass of the object
              
                planets_model[i].setRadius(radius);
                if (mass[i] <= 0.2) {
                    planets_model[i].setFillColor(sf::Color::Yellow);
                    planets_true[i].setOutlineColor(sf::Color::Yellow);
                }
                else if (mass[i] > 0.2 && mass[i] <= 0.45) {
                    planets_model[i].setFillColor(sf::Color::Green);
                    planets_true[i].setOutlineColor(sf::Color::Green);
                }
                else if (mass[i] > 0.45 && mass[i] <= 0.7) {
                    planets_model[i].setFillColor(sf::Color::Red);
                    planets_true[i].setOutlineColor(sf::Color::Red);
                }
                else {
                    planets_model[i].setFillColor(sf::Color::Blue);
                    planets_true[i].setOutlineColor(sf::Color::Blue);
                } // setting colour linked with size of the planet - for better visuality

                planets_true[i].setRadius(radius);
                planets_true[i].setFillColor(sf::Color::Transparent);
                planets_true[i].setOutlineThickness(2);//getting the middle of true position planets transparent 

                double x_new = 0.0, y_new = 0.0;
                if (i < positions_model.size() && !positions_model[i].empty()) {
                    if (currentFrame < positions_model[i].size()) {
                        x_new = (positions_model[i][currentFrame].x + 2.5) * (800.0 / 5.0);
                        y_new = (positions_model[i][currentFrame].y + 2.5) * (800.0 / 5.0);
                    }
                }
                planets_model[i].setPosition(x_new, y_new);//setting the real position for planet - from previously loaded file

                double x_AI_new = 0.0, y_AI_new = 0.0;
                if (i < positions_true.size() && !positions_true[i].empty()) {
                    if (currentFrame < positions_true[i].size()) {
                        x_AI_new = (positions_true[i][currentFrame].x + 2.5) * (800.0 / 5.0);
                        y_AI_new = (positions_true[i][currentFrame].y + 2.5) * (800.0 / 5.0);
                    }
                }
                planets_true[i].setPosition(x_AI_new, y_AI_new);

                window.draw(planets_true[i]);
                window.draw(planets_model[i]);
                indow.draw(planets[i]);
            }

            std::vector<sf::Text> texts(amount);
            for (int i = 0; i < amount; i++) {
                texts[i].setFont(font);
              
                texts[i].setCharacterSize(12);

                texts[i].setFillColor(sf::Color::White);

                std::ostringstream massString;
                massString << "Mass: " << mass[i];
                texts[i].setString(massString.str());
              
                texts[i].setPosition(planets_model[i].getPosition().x + 20, planets_model[i].getPosition().y - 20);
                window.draw(texts[i]);//displaying masses of the planets near them
            }

            sf::Text iterationText, instructionText;
            iterationText.setFont(font);
            iterationText.setCharacterSize(15);
            iterationText.setFillColor(sf::Color::White);
            iterationText.setPosition(700, 10);
            iterationText.setString("Iteration: " + std::to_string((currentIteration/2) + 1));
            window.draw(iterationText);//info about iteration we are currently in - top right corner

            instructionText.setFont(font);
            instructionText.setCharacterSize(15);
            instructionText.setFillColor(sf::Color::White);
            instructionText.setPosition(10, 10);
            instructionText.setString("In order to change iteration to the next one, press ->,\nif you want to see the previous iteration, press <-.");
            window.draw(instructionText);//info about how to navigate between iterations

            window.display();

            sf::Time frameTime = sf::seconds(updateTime);
            sf::sleep(frameTime); //frame update

            if (nextIteration) {
                currentIteration = (currentIteration + 2) % totalIterations;
                break;
            }
            else if (previousIteration) {
                currentIteration = (currentIteration - 2 + totalIterations) % totalIterations;
                break;
            }//changing of interation - based on if we pressed any button - we're changing 2 at once becouse of the file format

            currentFrame++;//implementing frame to display a new position of object

            if (currentFrame >= frames) {
                break;
            }
        }
    }
    return 0;
}
