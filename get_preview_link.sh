# cloud9用
ip=$(curl http://checkip.amazonaws.com)
echo "Flask App URL"
echo "http://$ip:5000"

echo "DB Admin URL"
echo "http://$ip:80"

echo "Mailhog URL"
echo "http://$ip:8025"