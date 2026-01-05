from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# 遊戲全局狀態（簡化版）
game_state = {
    "players": [],
    "current_turn": 0,
    "timer": 0,
    "board_size": 20,
    "questions": []
}

@app.route('/')
def index():
    return "<h1>大富翁遊戲首頁</h1><p>請至設定頁面配置遊戲</p>"

@app.route('/setup', methods=['POST'])
def setup_game():
    data = request.json
    game_state["players"] = [
        {"id": i, "name": f"玩家 {i+1}", "position": 0, "money": data['money']}
        for i in range(int(data['player_count']))
    ]
    game_state["timer"] = data['time_limit']
    game_state["questions"] = data['questions']
    return jsonify({"status": "success", "message": "遊戲已初始化"})

@app.route('/roll', methods=['GET'])
def roll_dice():
    # 模擬擲骰子與移動
    steps = random.randint(1, 6)
    player = game_state["players"][game_state["current_turn"]]
    player["position"] = (player["position"] + steps) % game_state["board_size"]
    
    # 切換玩家
    game_state["current_turn"] = (game_state["current_turn"] + 1) % len(game_state["players"])
    
    return jsonify({
        "player": player["name"],
        "roll": steps,
        "new_position": player["position"]
    })

if __name__ == '__main__':
    app.run(debug=True)