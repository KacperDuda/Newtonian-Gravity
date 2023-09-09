#include <SFML/Graphics.hpp>
#include <SFML/System.hpp>
#include <sstream>
#include <iostream>
#include <fstream>
#include <nlohmann/json.hpp>
#include <vector>

int main() {
    std::ifstream file("3-body-problem.json");
    if (!file.is_open()) {
        std::cerr << "Failed to open .json file" << std::endl;
        return 1;
    }

    nlohmann::json data;
    file >> data;

    int amount = data["amount"];
    int frames = data["frames"];

    sf::RenderWindow window(sf::VideoMode(800, 800), "test");

    std::vector<sf::CircleShape> planets(amount); //vector of planets - drawings
    std::vector<float> mass; //masses of planets in order
    std::vector<std::vector<sf::Vector2f>> positions; //vector of positions of planets in order of planets and in order of frames

    for (const auto& planetData : data["planets"]) {
        float mass_tmp = planetData["mass"];
        mass.push_back(mass_tmp); //importing and  setting masses of planets

        std::vector<sf::Vector2f> positions_tmp;
        for (const auto& positionData : planetData["positions"]) {
            float x = positionData["x"];
            float y = positionData["y"];
            positions_tmp.emplace_back(x, y);
        }
        positions.push_back(positions_tmp); // setting positions of planets in order
    }

    int currentFrame = 0;

    sf::Font font;
    if (!font.loadFromFile("arial.ttf")) { //loading font for displaying a text
        return EXIT_FAILURE;
    }

    sf::Clock clock;
    float updateTime = data["delta"]; // time in which frame will be updated
    float elapsedTime = 0.0f;

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed) {
                window.close();
            }
        }

        window.clear();

        for (int i = 0; i < amount; i++) {
            double radius = 10 * mass[i]; //setting radius which is linked with mass of object
            planets[i].setRadius(radius); 
            planets[i].setFillColor(sf::Color::Red);

            double x_new = 0.0, y_new = 0.0;

            if (i < positions.size() && !positions[i].empty()) {
                if (currentFrame < positions[i].size()) {
                    x_new = (positions[i][currentFrame].x + 2.5) * (800.0 / 5.0);
                    y_new = (positions[i][currentFrame].y + 2.5) * (800.0 / 5.0);
                }
            }
            planets[i].setPosition(x_new, y_new);//setting positions for planets

            window.draw(planets[i]);
        }

        std::vector<sf::Text> texts(amount);
        for (int i = 0; i < amount; i++) {
            texts[i].setFont(font);
            texts[i].setCharacterSize(15);
            texts[i].setFillColor(sf::Color::White);

            std::ostringstream massString;
            massString << "Mass: " << mass[i];
            texts[i].setString(massString.str());
            texts[i].setPosition(planets[i].getPosition().x + 30, planets[i].getPosition().y - 30);
            window.draw(texts[i]);//displaying a text with info about planet
        }

        currentFrame++; // changing frame - changing position

        window.display();

        float deltaTime = clock.restart().asSeconds();
        elapsedTime += deltaTime;

        if (currentFrame > frames) {
            window.close();
        }
        elapsedTime = 0.0f;
    }
    return 0;
}
