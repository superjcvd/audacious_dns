-- https://gist.github.com/henriquegogo/fa22ffec3eb345540ef2
driver = require "luasql.sqlite3"
env = assert (driver.sqlite3())
-- con = assert (env:connect("/var/audacious_dns_test/audacious_dns.db"))
con = assert (env:connect("/var/audacious_dns/database/database.db"))


function preresolve(dq)

    -- extract 2nd level DNS record (ie: google.com)
    -- remove the trailing dot
    local domain  = (dq.qname:toString()):sub(1,-2)
    -- pdnslog(domain, pdns.loglevels.Info)

    -- if( domain == 'mco.mineplex.com' ) then
    --     pdnslog("minecraft hook", pdns.loglevels.Info)
    --     dq.rcode=0 -- make it a normal answer
    --     dq:addAnswer(pdns.A, "192.168.0.250")
    --     return true
    -- end

    -- local top_domain = domain:match(".*%.(%w+%.%w+)")
    -- local prefix,top_domain = domain:match("([%w%-%.])(%w+%.%w+)$")
    local prefix,top_domain = domain:match("([.*%.]-)(%w+%.%w+)$")
    -- pdnslog(string.format("[%s][%s]",prefix,top_domain), pdns.loglevels.Info)

    -- prepare the sql query and execute
    local request = string.format(
        [[SELECT domain_id, domain_isactive FROM domains 
        WHERE domain_name LIKE '%s';]]
        , con:escape( domain ))
    -- pdnslog(request, pdns.loglevels.Info)
    local result, error = exec_sql(request)
    -- if result is a non empty array of objets
    local next = next
    if next(result) then
        -- extract first line of sql result to get the domain
        local domain_id = result[1].domain_id
        local client_ip = dq.remoteaddr:toString()
        local stats_id  = client_ip .. '.' .. domain_id
        pdnslog("domain found in blacklist - updating stats...", pdns.loglevels.Info)
        pdnslog(domain_id, pdns.loglevels.Info)

        -- Update DNS statistics in a thread for better perfs
        -- update_statistics(stats_id, domain_id, client_ip)
        local thread = coroutine.create(update_statistics)
        coroutine.resume(thread, stats_id, domain_id, client_ip)

        dq.rcode=0 -- make it a normal answer
        dq:addAnswer(pdns.A, "127.0.0.1")
        -- con:close()
        return true
    else
        -- pdnslog("domain not found in blacklist", pdns.loglevels.Info)
        -- con:close()
        return false
    end
end


function update_statistics(stats_id, domain_id, client_ip)
    local request = string.format(
        [[INSERT INTO statistics (stats_id, stats_domain_id, stats_client_ip, stats_request_count)
        VALUES ( '%s', %s, '%s', %s )
        ON CONFLICT(stats_id) DO UPDATE SET stats_request_count = stats_request_count + 1;]]
        , stats_id, domain_id, client_ip, 1)
        pdnslog(request)

    local result, error = exec_sql(request)
end


function exec_sql(request)
    local sql_result = {}
    local sql_error = ""
    local sql_cursor, sql_error = assert (con:execute( request ))
    if sql_error then
        sql_cursor:close()
        return sql_result, sql_error
    end

    if type(sql_cursor) == "number" then
        return sql_cursor, sql_error
    else
        -- get all lines in an array
        local row = {}
        while sql_cursor:fetch(row, "a") do
            sql_result[#sql_result+1] = row
        end
        sql_cursor:close()
        return sql_result, sql_error
    end

end