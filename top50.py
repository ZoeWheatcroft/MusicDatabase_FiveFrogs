import dbaccess
from userfollow import print_list

def top50_header(dash_len):
    list_name = "~*~ Top 50 Charts ~*~"
    print_list(list_name, dash_len)
    line = "-" * dash_len
    print("%18s | %18s | %10s | %10s" % ("Rank","Artist Name", "Song Title", "Album"))
    print(line)

# Returns the top 50 most popular songs in the last 30 days (rolling)
def find_top50_recent():
    lst = dbaccess.execute_query("SELECT s.title \
                                FROM song AS s \
                                ORDER BY s.listen_count DESC \
                                LIMIT 50")
    dash_len = 70
    top50_header(dash_len)

# Returns the top 50 most popular songs among my friends
def find_top50_friends():
    return

if __name__ == '__main__':
    find_top50_recent()